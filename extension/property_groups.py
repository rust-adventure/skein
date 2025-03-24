import base64
import hashlib
import sys
import bpy # type: ignore
import re
import inspect

# the class we use to create PropertyGroups dynamically
class ComponentData(bpy.types.PropertyGroup):
    type_path: bpy.props.StringProperty(name="type_path", default="Unknown") # type: ignore
    name: bpy.props.StringProperty(name="Name", default="Unknown") # type: ignore

# capitalize a word without lowercasing the result
# of the word. This means TeamMember stays and doesn't
# turn into Teammember
def cap(val):
  return val[0].upper() + val[1:]

def capitalize_path(s):
    return "".join(map(cap, re.split('[:_]+', s)))

# PropertyGroup classes can't be more than 64 characters,
# so try to squeeze under the limit by hashing the capitalized
# paths.
def hash_type_path(data):
    m = hashlib.md5(data.encode('ascii'))
    base64_bytes = base64.b16encode(m.digest())
    output = base64_bytes.decode("ascii")
    return "SKEIN_" + output

def make_property(
        skein_property_groups,
        registry,
        original_type_path,
        override_component=None
):
    """build a subclass of ComponentData or return a "scalar" property
    The subclass is a PropertyGroup that we can build up when we fetch the registry,
    The UI to editor a type is built from these PropertyGroup classes

    @param: skein_property_groups All of the property groups constructed so far. Will mutate this to add more property groups.
    @param: registry dict representation of the Bevy registry information
    @param: original_type_path Either a full type_path (`component_tests::SomeThings::OneThing`) or a type_path with `#/#defs/alloc` on the front
    @param: override_component An optional value that is used when you have access to the registry type information but that registry type information is not directly accessible by registry[type_path]. This happens in complex enums. (default None)
    """

    'unittest' in sys.modules.keys()
    preferences = bpy.context.preferences
    debug = False
    if 'unittest' not in sys.modules.keys():
        debug = preferences.addons["bl_ext.user_default.bevy_skein"].preferences.debug

    type_path = original_type_path.removeprefix("#/$defs/")
    component = override_component if override_component != None else registry[type_path]

    if type_path in skein_property_groups:
        # The type was already constructed and can be 
        # returned from the "cache" instead of being
        # created again
        return skein_property_groups[type_path]

    if debug:
        print("\nmake_property::", type_path)

    if debug:
        print(component)

    if "kind" not in component:
        print("kind not in ", type_path, component)
    match component["kind"]:
        case "Array":
            print("Array is unimplemented in make_property: ", type_path)
            return
        case "Enum":
            if debug:
                print("Enum: ", component["type"])
            match component["type"]:
                case "string":
                    items = []
                    for item in component["oneOf"]:
                        items.append((item, item, ""))

                    if debug:
                        print(items)

                    # TODO: make an enum default value
                    skein_property_groups[type_path] = bpy.props.EnumProperty(
                        items=items,
                        override={"LIBRARY_OVERRIDABLE"},
                    )

                    return skein_property_groups[type_path]
                case "object":
                    annotations = {}
                    items = []

                    # Take the shortPath as the dropdown ui option
                    for item in component["oneOf"]:
                        items.append((item["shortPath"], item["shortPath"], ""))

                    if debug:
                        print(items)

                    # TODO: set default for skein_enum_index?
                    annotations["skein_enum_index"] = bpy.props.EnumProperty(
                        name="variant",
                        items=items,
                        override={"LIBRARY_OVERRIDABLE"},
                    )

                    for option in component["oneOf"]:
                        if debug:
                            print("- option: ", option["shortPath"])
                        key = option["shortPath"]

                        if (key == "None" and component["modulePath"] == "core::option") or ("kind" not in option):
                            # this is the None variant of a core::option::Option
                            # so we'll leave it out of the annotations and 
                            # keep it in the `skein_enum_index` so the user can
                            # select it, but there's no value to edit
                            pass
                        else:
                            property = make_property(
                                skein_property_groups,
                                registry,
                                option["typePath"],
                                option
                            )
                            if inspect.isclass(property):
                                annotations[key] = bpy.props.PointerProperty(
                                    type=property,
                                    override={"LIBRARY_OVERRIDABLE"},
                                )
                            else:
                                annotations[key] = property

                    # add this struct type to the skein_property_groups so it 
                    # can be accessed elsewhere by type_path
                    skein_property_groups[type_path] = type(hash_type_path(capitalize_path(type_path)), (ComponentData,), {
                        '__annotations__': annotations,
                    })

                    # registering the class is required for certain Blender
                    # functionality to work.
                    if debug:
                        print("REGISTERING: " + type_path)
                    bpy.utils.register_class(
                        skein_property_groups[type_path]
                    )

                    # return the type we just constructed
                    return skein_property_groups[type_path]
                case _:
                    print("unknown Enum type: ", component["type"], "\n  ", type_path)
                    return
        case "List":
            print("List is unimplemented in make_property: ", type_path)
            return
        case "Map":
            print("Map is unimplemented in make_property: ", type_path)
            return
        case "Set":
            print("Set is unimplemented in make_property: ", type_path)
            return
        case "Struct":
            annotations = {}
            # only recurse if we have properties to set, otherwise
            # annotations should be an empty object
            if "properties" in component:
                for key in component["properties"]:
                    if debug:
                        print("- key: ", key)
                    property = make_property(
                        skein_property_groups,
                        registry,
                        component["properties"][key]["type"]["$ref"]
                    )
                    if inspect.isclass(property):
                        annotations[key] = bpy.props.PointerProperty(
                            type=property,
                            override={"LIBRARY_OVERRIDABLE"},
                        )
                    else:
                        annotations[key] = property

            def type_override():
                return type_path
            # add this struct type to the skein_property_groups so it 
            # can be accessed elsewhere by type_path
            t = hash_type_path(capitalize_path(type_path))
            skein_property_groups[type_path] = type(t, (ComponentData,), {
                '__annotations__': annotations,
                'type_override': type_override
            })

            # registering the class is required for certain Blender
            # functionality to work.
            if debug:
                print("REGISTERING: " + type_path)
            bpy.utils.register_class(
                skein_property_groups[type_path]
            )

            # return the type we just constructed
            return skein_property_groups[type_path]
        case "Tuple":
            if len(component["prefixItems"]) == 1:
                skein_property_groups[type_path] = make_property(
                    skein_property_groups,
                    registry,
                    component["prefixItems"][0]["type"]["$ref"]
                )
                return skein_property_groups[type_path]
            else:
                print("Tuple is unimplemented in make_property for lengths longer than 1 element: ", type_path)
                return
        case "TupleStruct":
            # single element tuple struct is a special case
            # because the reflection format treats it as a
            # single value for the type_path key
            # ```
            # { "skein::tests::TupleStruct": 12 }
            # ```
            if len(component["prefixItems"]) == 1:
                print("Single Element TupleStruct")
                skein_property_groups[type_path] = make_property(
                    skein_property_groups,
                    registry,
                    component["prefixItems"][0]["type"]["$ref"]
                )
                print("succeeded", type_path)
                return skein_property_groups[type_path]
            else:
                print("TupleStruct is unimplemented in make_property for lengths longer than 1 element: ", type_path)
                return
        case "Value":
            # print("- component[type]:  ", component["type"])
            match component["type"]:
                case "boolean":
                    return bpy.props.BoolProperty(
                        override={"LIBRARY_OVERRIDABLE"}
                    )
                case "uint":
                    match type_path:
                        case "u8":
                            return bpy.props.IntProperty(
                                min=0,
                                max=255,
                                override={"LIBRARY_OVERRIDABLE"},
                            )
                        case "u16":
                            return bpy.props.IntProperty(
                                min=0,
                                max=65535,
                                override={"LIBRARY_OVERRIDABLE"},
                            )
                        case "u32":
                            return bpy.props.IntProperty(
                                min=0,
                                # blender actually sets the default hard maximum to
                                # 2^31, not 2^32, so not sure if we can even set
                                # those numbers from inside blender
                                # max=4294967295,
                                override={"LIBRARY_OVERRIDABLE"},
                        )
                        case "u64":
                            return bpy.props.IntProperty(
                                min=0,
                                # blender actually sets the default hard maximum to
                                # 2^31, not 2^32, so not sure if we can even set
                                # those numbers from inside blender
                                # max=4294967295,
                                override={"LIBRARY_OVERRIDABLE"},
                        )
                        case "u128":
                            return bpy.props.IntProperty(
                                min=0,
                                # blender actually sets the default hard maximum to
                                # 2^31, not 2^32, so not sure if we can even set
                                # numbers bigger than this for u128 in Blender
                                override={"LIBRARY_OVERRIDABLE"},
                        )
                        case "usize":
                            return bpy.props.IntProperty(
                                min=0,
                                # blender actually sets the default hard maximum to
                                # 2^31, not 2^32, so not sure if we can even set
                                # those numbers from inside blender
                                # max=4294967295,
                                override={"LIBRARY_OVERRIDABLE"},
                        )
                        case _:
                            print("unknown uint type: ", type_path)
                            return bpy.props.IntProperty(
                                min=0,
                                override={"LIBRARY_OVERRIDABLE"}
                            )
                case "int":
                    match type_path:
                        case "i8":
                            return bpy.props.IntProperty(
                                min=-128,
                                max=127,
                                override={"LIBRARY_OVERRIDABLE"},
                            )
                        case "i16":
                            return bpy.props.IntProperty(
                                min=-32_768,
                                max=32_767,
                                override={"LIBRARY_OVERRIDABLE"},
                            )
                        case "i32":
                            return bpy.props.IntProperty(
                                min=-2_147_483_648,
                                max=2_147_483_647,
                                override={"LIBRARY_OVERRIDABLE"},
                        )
                        case "i64":
                            return bpy.props.IntProperty(
                                override={"LIBRARY_OVERRIDABLE"},
                            )
                        case "isize":
                            return bpy.props.IntProperty(
                                override={"LIBRARY_OVERRIDABLE"},
                            )
                        case _:
                            print("unknown iint type: ", type_path)
                            return bpy.props.IntProperty(
                                min=0,
                                override={"LIBRARY_OVERRIDABLE"},
                            )
                case "float":
                    return bpy.props.FloatProperty(
                        override={"LIBRARY_OVERRIDABLE"},
                    )
                case "string":
                    return bpy.props.StringProperty(
                        override={"LIBRARY_OVERRIDABLE"},
                    )
                case "object":
                    if debug:
                        print("component: ", component)
                    match component["typePath"]:
                        case "core::num::NonZeroU8":
                            return bpy.props.IntProperty(
                                min=0,
                                max=255,
                                default=1,
                                override={"LIBRARY_OVERRIDABLE"},
                            )
                        case "core::num::NonZeroU16":
                            return bpy.props.IntProperty(
                                min=1,
                                max=65535,
                                 default=1,
                                override={"LIBRARY_OVERRIDABLE"},
                            )
                        case "core::num::NonZeroU32":
                            return bpy.props.IntProperty(
                                min=1,
                                default=1,
                                override={"LIBRARY_OVERRIDABLE"},
                            )
                        case "core::num::NonZeroU64":
                            return bpy.props.IntProperty(
                                min=1,
                                default=1,
                                override={"LIBRARY_OVERRIDABLE"},
                            )
                        # TODO: prevent 0 from being valid for NonZeroI* values, but how?
                        case "core::num::NonZeroI8":
                            return bpy.props.IntProperty(
                                min=-128,
                                max=127,
                                default=1,
                                override={"LIBRARY_OVERRIDABLE"},
                            )
                        case "core::num::NonZeroI16":
                            return bpy.props.IntProperty(
                                min=-32_768,
                                max=32_767,
                                default=1,
                                override={"LIBRARY_OVERRIDABLE"},
                            )
                        case "core::num::NonZeroI32":
                            return bpy.props.IntProperty(
                                min=-2_147_483_648,
                                max=2_147_483_647,
                                default=1,
                                override={"LIBRARY_OVERRIDABLE"},
                        )
                        case "core::num::NonZeroI64":
                            return bpy.props.IntProperty(
                                default=1,
                                override={"LIBRARY_OVERRIDABLE"},
                            )
                        case "smol_str::SmolStr":
                            return bpy.props.StringProperty(
                                override={"LIBRARY_OVERRIDABLE"},
                            )
                        case "alloc::borrow::Cow<str>":
                            return bpy.props.StringProperty(
                                override={"LIBRARY_OVERRIDABLE"},
                            )
                        case "avian3d::collision::collider::parry::TrimeshFlags":
                            # TODO: What do we do about this. hard coding third-party crate
                            # primitive Value handling is... not great. Can we figure out
                            # how to insert this data into the reflection information?
                            # its opaque intentionally, so really this is a set of checkboxes
                            # represented as a bitfield and the UI should reflect that.
                            return bpy.props.IntProperty(
                                min=0,
                                max=255,
                                override={"LIBRARY_OVERRIDABLE"},
                            )
                        case "core::time::Duration" | "bevy_utils::Duration":
                            # Duration {
                            #     secs: u64,
                            #     nanos: Nanoseconds, // Always 0 <= nanos < NANOS_PER_SEC
                            # }
                            annotations = {}
                            annotations["secs"] = bpy.props.IntProperty(
                                    name="secs",
                                    min=0,
                                    # blender actually sets the default hard maximum to
                                    # 2^31, not 2^32, so not sure if we can even set
                                    # those numbers from inside blender
                                    # max=4294967295,
                                    override={"LIBRARY_OVERRIDABLE"},
                            )

                            # NANOS_PER_SEC == 1_000_000_000
                            # so nanos must be: 0..=999_999_999
                            annotations["nanos"] = bpy.props.IntProperty(
                                    name="nanos",
                                    min=0,
                                    max=999999999,
                                    override={"LIBRARY_OVERRIDABLE"},
                            )
                                        
                            # add this struct type to the skein_property_groups so it 
                            # can be accessed elsewhere by type_path
                            t = capitalize_path(type_path)
                            skein_property_groups[type_path] = type(t, (ComponentData,), {
                                '__annotations__': annotations,
                            })

                            # registering the class is required for certain Blender
                            # functionality to work.
                            # if debug:
                            print("REGISTERING: " + type_path)
                            bpy.utils.register_class(
                                skein_property_groups[type_path]
                            )

                            # return the type we just constructed
                            return skein_property_groups[type_path]
                        case _:
                            # if debug:
                            print("unhandled `Value` of `object` type: ", component["typePath"], "\n  ", type_path)
                            return
                case _:
                    # if debug:
                    print("unhandled type: ", component["type"])
                    return
        # If an exact match is not confirmed, this last case will be used if provided
        case _:
            # if debug:
            print("unhandled kind:", component["kind"], "\n  ", type_path)
            return "Something's wrong with the world"
