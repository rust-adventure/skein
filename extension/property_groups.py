import bpy
import re
import inspect
from .form_to_object import update_component_data

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

    type_path = original_type_path.removeprefix("#/$defs/")
    component = override_component if override_component != None else registry[type_path]

    if type_path in skein_property_groups:
        # The type was already constructed and can be 
        # returned from the "cache" instead of being
        # created again
        return skein_property_groups[type_path]

    print("\nmake_property::", type_path)

    match component["kind"]:
        case "Array":
            print("Array is unimplemented in make_property")
            return
        case "Enum":
            print("Enum: ", component["type"])
            match component["type"]:
                case "string":
                    items = []
                    for item in component["oneOf"]:
                        items.append((item, item, ""))

                    print(items)

                    # TODO: make an enum default value
                    skein_property_groups[type_path] = bpy.props.EnumProperty(
                        items=items,
                        update=update_component_data
                    )

                    return skein_property_groups[type_path]
                case "object":
                    annotations = {}
                    items = []

                    # Take the shortPath as the dropdown ui option
                    for item in component["oneOf"]:
                        items.append((item["shortPath"], item["shortPath"], ""))

                    print(items)

                    annotations["skein_enum_index"] = bpy.props.EnumProperty(
                        name="variant",
                        items=items,
                        update=update_component_data
                    )

                    for option in component["oneOf"]:
                        print("- option: ", option["shortPath"])
                        key = option["shortPath"]
                        property = make_property(
                            skein_property_groups,
                            registry,
                            option["typePath"],
                            option
                        )
                        if inspect.isclass(property):
                            annotations[key] = bpy.props.PointerProperty(type=property)
                        else:
                            annotations[key] = property

                    # add this struct type to the skein_property_groups so it 
                    # can be accessed elsewhere by type_path
                    skein_property_groups[type_path] = type(capitalize_path(type_path), (ComponentData,), {
                        '__annotations__': annotations,
                    })

                    # registering the class is required for certain Blender
                    # functionality to work.
                    print("REGISTERING: " + type_path)
                    bpy.utils.register_class(
                        skein_property_groups[type_path]
                    )

                    # return the type we just constructed
                    return skein_property_groups[type_path]
                case _:
                    print("unknown Enum type")
                    return
        case "List":
            print("List is unimplemented in make_property")
            return
        case "Map":
            print("Map is unimplemented in make_property")
            return
        case "Set":
            print("Set is unimplemented in make_property")
            return
        case "Struct":
            annotations = {}
            # only recurse if we have properties to set, otherwise
            # annotations should be an empty object
            if "properties" in component:
                for key in component["properties"]:
                    print("- key: ", key)
                    property = make_property(
                        skein_property_groups,
                        registry,
                        component["properties"][key]["type"]["$ref"]
                    )
                    if inspect.isclass(property):
                        annotations[key] = bpy.props.PointerProperty(type=property)
                    else:
                        annotations[key] = property

            # add this struct type to the skein_property_groups so it 
            # can be accessed elsewhere by type_path
            skein_property_groups[type_path] = type(capitalize_path(type_path), (ComponentData,), {
                '__annotations__': annotations,
            })

            # registering the class is required for certain Blender
            # functionality to work.
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
                print("Tuple is unimplemented in make_property for lengths longer than 1 element")
                return
        case "TupleStruct":
            # single element tuple struct is a special case
            # because the reflection format treats it as a
            # single value for the type_path key
            # ```
            # { "skein::tests::TupleStruct": 12 }
            # ```
            if len(component["prefixItems"]) == 1:
                skein_property_groups[type_path] = make_property(
                    skein_property_groups,
                    registry,
                    component["prefixItems"][0]["type"]["$ref"]
                )
                return skein_property_groups[type_path]
            else:
                print("TupleStruct is unimplemented in make_property for lengths longer than 1 element")
                return
        case "Value":
            # print("- component[type]:  ", component["type"])
            match component["type"]:
                case "uint":
                    match type_path:
                        case "u8":
                            return bpy.props.IntProperty(
                                min=0,
                                max=255,
                                update=update_component_data
                            )
                        case "u16":
                            return bpy.props.IntProperty(
                                min=0,
                                max=65535,
                                update=update_component_data
                            )
                        case "u32":
                            return bpy.props.IntProperty(
                                min=0,
                                # blender actually sets the default hard maximum to
                                # 2^31, not 2^32, so not sure if we can even set
                                # those numbers from inside blender
                                # max=4294967295,
                                update=update_component_data
                        )
                        case "u64":
                            return bpy.props.IntProperty(
                                min=0,
                                # blender actually sets the default hard maximum to
                                # 2^31, not 2^32, so not sure if we can even set
                                # those numbers from inside blender
                                # max=4294967295,
                                update=update_component_data
                        )
                        case "usize":
                            return bpy.props.IntProperty(
                                min=0,
                                # blender actually sets the default hard maximum to
                                # 2^31, not 2^32, so not sure if we can even set
                                # those numbers from inside blender
                                # max=4294967295,
                                update=update_component_data
                        )
                        case _:
                            print("unknown uint type: ", type_path)
                            return bpy.props.IntProperty(min=0, update=update_component_data)
                case "int":
                    match type_path:
                        case "i8":
                            return bpy.props.IntProperty(
                                min=-128,
                                max=127,
                                update=update_component_data
                            )
                        case "i16":
                            return bpy.props.IntProperty(
                                min=-32_768,
                                max=32_767,
                                update=update_component_data
                            )
                        case "i32":
                            return bpy.props.IntProperty(
                                min=-2_147_483_648,
                                max=2_147_483_647,
                                update=update_component_data
                        )
                        case "i64":
                            return bpy.props.IntProperty(update=update_component_data)
                        case "isize":
                            return bpy.props.IntProperty(update=update_component_data)
                        case _:
                            print("unknown iint type: ", type_path)
                            return bpy.props.IntProperty(min=0, update=update_component_data)
                case "float":
                    return bpy.props.FloatProperty(update=update_component_data)
                case "string":
                    return bpy.props.StringProperty(update=update_component_data)
                case "object":
                    match component["type_path"]:
                        case "core::time::Duration":
                            print("core::time::Duration is currently not handled")
                            return
                        case _:
                            print("unhandled `Value` of `object` type: ", component["type_path"])
                            return
                case _:
                    print("unhandled type: ", component["type"])
                    return
        # If an exact match is not confirmed, this last case will be used if provided
        case _:
            print("unhandled kind:", component["kind"])
            return "Something's wrong with the world"
