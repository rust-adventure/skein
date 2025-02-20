import bpy
import requests
import json
import re
import inspect

registry_filepath = "/Users/chris/github/christopherbiscardi/skein/skein-registry.json"

def update_component_data(self, context):
    # context.obj.skein.something
    print("updating component data")
    obj = context.object
    obj_skein = obj["skein"]
    active_component_index = obj.active_component_index
    global_skein = context.window_manager.skein
    registry = json.loads(global_skein.registry)
    skein_property_groups = context.window_manager.skein_property_groups
    active_component = obj_skein[active_component_index]
    type_path = active_component["type_path"]
    active_editor = context.window_manager.active_editor

    if obj_skein:
        active_component_data = obj_skein[active_component_index]
        type_path = active_component_data["type_path"]
        registry_component_reflection_data = registry[type_path]
        
        if type_path in skein_property_groups:
            if inspect.isclass(skein_property_groups[type_path]):
                # TODO: this may only work for Structs
                component_fields = inspect.get_annotations(skein_property_groups[type_path])
                new_data = {}
                for key in component_fields:
                    new_data[key] = active_editor[key]
                    print(new_data)
                    active_component["value"] = json.dumps(new_data)
            else:
                active_component["value"] = json.dumps(active_editor)

class ComponentTypeData(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name", default="Unknown")
    value: bpy.props.StringProperty(name="Value", default="Unknown")
    type_path: bpy.props.StringProperty(name="Type Path", default="Unknown")
    short_path: bpy.props.StringProperty(name="Short Path", default="Unknown")

class ComponentData(bpy.types.PropertyGroup):
    type_path: bpy.props.StringProperty(name="type_path", default="Unknown")
    name: bpy.props.StringProperty(name="Name", default="Unknown")
    value: bpy.props.StringProperty(name="Component Data")

class PGSkeinWindowProps(bpy.types.PropertyGroup):
    registry: bpy.props.StringProperty(name="Bevy Registry", default="{}")
    components: bpy.props.CollectionProperty(type=ComponentTypeData)


def update_component_form(self, context):
    print("\n## update component form")
    obj = context.object
    obj_skein = obj["skein"]
    active_component_index = obj.active_component_index
    global_skein = context.window_manager.skein
    registry = json.loads(global_skein.registry)
    skein_property_groups = context.window_manager.skein_property_groups
    active_component = obj_skein[active_component_index]
    type_path = active_component["type_path"]

    # active_component.__dict__["value"] = bpy.props.StringProperty(default="hello")
    # print(skein_property_groups[type_path])
    # print(skein_property_groups[type_path].__annotations__)
    # TODO: What happens when we get data from object
    # and insert it
    if inspect.isclass(skein_property_groups[type_path]):
        bpy.types.WindowManager.active_editor = bpy.props.PointerProperty(
            type=skein_property_groups[type_path],
        )
    else:
        bpy.types.WindowManager.active_editor = skein_property_groups[type_path]
    print("active_component_index", active_component_index)

def on_select_new_component(self, context):
    """Executed when a new component is selected for insertion onto an object"""
    print("\n####### on_select_new_component")
    selected_component = context.window_manager.selected_component;
    global_skein = context.window_manager.skein
    if global_skein.registry:
        print("\nregistry character:")
        data = json.loads(global_skein.registry)
        if len(data.keys()) > 0:
            # print(data["event_ordering::PowerLevel"])
            print(data[selected_component])
        else:
            print("no data in registry")
    print("######\n")
    

# --------------------------------- #
#  Fetch and store the bevy type    #
#  registry, for panel display      #
# --------------------------------- #

class FetchBevyTypeRegistry(bpy.types.Operator):
    """Fetch the Bevy type registry via the Bevy Remote Protocol"""
    bl_idname = "bevy.fetch_type_registry" # unique identifier. not specially named
    bl_label = "Fetch Bevy Type Registry" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    # execute is called to run the operator
    def execute(self, context):
        print("\nexecute: FetchBevyTypeRegistry")
        # scene = context.scene
        # cursor = scene.cursor.location
        # obj = context.active_object
        global_skein = context.window_manager.skein
        skein_property_groups = context.window_manager.skein_property_groups

        data = {"jsonrpc": "2.0", "method": "bevy/registry/schema", "params": {}}
        r = requests.post('http://127.0.0.1:15702', json=data)
        brp_response = r.json()

        # If the bevy remote protocol returns an error, report it to the user
        if "error" in brp_response:
            print("bevy request errored out", brp_response["error"])
            self.report({"ERROR"}, "request for Bevy registry data errored out, is the Bevy Remote Protocol Plugin added and is the Bevy app running? :: " + json["error"]["message"])

        with open(registry_filepath,"w") as outfile:
            json.dump(brp_response["result"], outfile)
            print(outfile)

        global_skein.registry = json.dumps(brp_response["result"])

        component_list = []

        global_skein.components.clear()
        for k, value in brp_response["result"].items():
            # TODO: this must apply to all components
            # make_property is recursive, so all dependent types
            # should make it into the skein_property_groups
            if k == "component_tests::Player" or k == "component_tests::TaskPriority":
                # TODO: is registering classes here enough, or
                # are there more types in the recursive make_property
                # that need to be registered?
                print("\n make_property", k)
                new_property = make_property(
                    skein_property_groups,
                    brp_response["result"],
                    k
                )
                # if its a class we constructed, it has
                # to be registered. If its not, it can't
                # be registered without errors
                if inspect.isclass(new_property):
                    bpy.utils.register_class(
                        new_property
                    )

            if "reflectTypes" in value and "Component" in value["reflectTypes"]:
                component = global_skein.components.add()
                component.name = k
                component.value = k
                component.type_path = k
                component.short_path = value["shortPath"]

                component_list.append((k, value["shortPath"], k))

        bpy.types.WindowManager.skein_components = bpy.props.EnumProperty(
            items=component_list,
            description="A Component to add to the object",
            # default="()",
            # update=execute_operator
        )

        print("execute/end: FetchBevyTypeRegistry\n")

        # blender uses strings to indicate when operation is done
        return {'FINISHED'}

# --------------------------------- #
#  Add hardcoded test component     #
#  to object                        #
# --------------------------------- #

class InsertBevyComponent(bpy.types.Operator):
    """Insert a hardcoded component on the object (for development)"""
    bl_idname = "bevy.insert_bevy_component" # unique identifier. not specially named
    bl_label = "Insert Bevy Component (Dev)" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    # execute is called to run the operator
    def execute(self, context):
        print("\nexecute: InsertBevyComponent")
        # scene = context.scene
        # cursor = scene.cursor.location
        obj = context.active_object
        global_skein = context.window_manager.skein
        selected_component = context.window_manager.selected_component
        obj_skein = obj.skein
        # if the skein custom property doesn't exist,
        # create it.
        # if "skein" not in obj.id_data:
        #     obj.id_data["skein"] = {};
        
        # insert a component value
        # components are unique per-entity,
        # so a dict where the keys are components makes
        # sense here
        # obj.id_data["skein"]["event_ordering::Character"] = {
        #     "name": "Hollow Knight"
        # }

        if global_skein.registry:
            registry = json.loads(global_skein.registry)
            if list(registry) and registry[selected_component]:
                data = registry[selected_component]
                print(data)
                component = obj.skein.add()
                component.name = data["shortPath"]
                component.type_path = selected_component
                # TODO: This needs to be the default data for a given component
                # component.value = json.dumps({
                #     "name": "Hollow Knight"
                # })
                # If we inserted a new component, update the 
                # active_component_index to show the right editor
                # for the newly inserted component
                obj.active_component_index = len(obj_skein) - 1

            else:
                print("no data in registry")
        else:
            print("no global registry set")


        print("execute/end: InsertBevyComponent\n")
        # blender uses strings to indicate when operation is done
        return {'FINISHED'}

# ---------------------------------- #
#  Skein Panel for adding components #
# ---------------------------------- #

class SkeinPanel(bpy.types.Panel):
    """Creates a Panel in the Object Properties window"""
    bl_label = "Skein Bevy Panel"
    bl_idname = "OBJECT_PT_skein"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'object'

    def draw(self, context):
        # print("\ndraw: SkeinPanel")
        layout = self.layout
        obj = context.object
        obj_skein = obj.skein
        active_component_index = obj.active_component_index
        global_skein = context.window_manager.skein
        # TODO: the registry can likely be loaded into a dict in a less
        # common place. This function runs every draw
        registry = json.loads(global_skein.registry)
        skein_property_groups = context.window_manager.skein_property_groups


        # row = layout.row()
        # row.label(text="Testing Skein!", icon='WORLD_DATA')

        # row = layout.row()
        # row.label(text="Active object is: " + obj.name)
        # row = layout.row()
        # row.prop(obj, "name")
        row = layout.row()
        
        # if "skein" in obj:
        # print("\nSkeinPanel object custom props:")
        # for key in obj.skein:
            # print(key.name)
            # print(key.type_path)
            # print(key.value)

        # print(bpy.types.WindowManager.skein.registry)
        # if global_skein.registry:
        #     print("\n# Components On Object:")
        #     registry = json.loads(global_skein.registry)
        #     if list(registry):
        #         for component in obj.skein:
        #             print(registry[component.type_path])
        #     else:
        #         print("no data in registry")

        # row.prop(context.window_manager, "skein_components")
        row.prop_search(
            context.window_manager,
            'selected_component',
            global_skein,
            "components",
            text="C:"
        )

        row = layout.row()
        row.operator("bevy.insert_bevy_component")

        layout.template_list(
            "UI_UL_list",
            "components list",
            obj,
            "skein",
            obj,
            "active_component_index"
        )


        box = layout.box()
        # obj_skein is an array of component data
        # empty lists are falsey
        if obj_skein:
            active_component_data = obj_skein[active_component_index]
            box.label(text=active_component_data["type_path"], icon='DOT')
            type_path = active_component_data["type_path"]
            registry_component_reflection_data = registry[type_path]
            active_editor = active_component_data
            # Marker component
            if "properties" not in registry_component_reflection_data and registry_component_reflection_data["kind"] == "Struct":
                box.label(text="Marker components have no data")
            
            if type_path in skein_property_groups:
                # TODO: this may only work for Structs
                component_fields = inspect.get_annotations(skein_property_groups[type_path])
                if inspect.isclass(context.window_manager.active_editor):
                    for key in component_fields:
                        print("key in component_fields: ", key)
                        # box.prop(obj_skein[active_component_index], key)
                        box.prop(context.window_manager.active_editor, key)
                else:
                    box.prop(context.window_manager, "active_editor")
                if "value" in active_component_data:
                    box.prop(active_component_data, "value")
            else:
                box.label(text="No property group for " + type_path)
        # match registry_component_reflection_data["kind"]:
        #     case "Struct":
        #         # no "properties" means its a marker component with no data
        #         if "properties" not in registry_component_reflection_data:
        #             box.label(text="Marker components have no data")
        #         else:
        #             print("TODO: Struct")
        #         pass
        #     case "Enum":
        #         pass
        #     case "List":
        #         pass
        #     case "Map":
        #         pass
        #     case "Set":
        #         pass
        #     case "Struct":
        #         pass
        #     case "Tuple":
        #         pass
        #     case "TupleStruct":
        #         #   "prefixItems": [{ "type": { "$ref": "#/$defs/u32" } }],
        #         for item in registry_component_reflection_data["prefixItems"]:
        #             print(item["type"]["$ref"])
        #     case "Value":
        #         pass
        #     # If an exact match is not confirmed, this last case will be used if provided
        #     case _:
        #         box.label(text="Something's wrong")

        # print(dir(context.window_manager.my_prop_grp.__annotations__))


        # print("draw/end: SkeinPanel\n")


# --------------------------------- #
#  Registration and unregistration  #
# --------------------------------- #

# add to the Blender menus
def menu_func(self, context):
    self.layout.operator(FetchBevyTypeRegistry.bl_idname)

def register():
    print("\n--------\nregister")
    # data types that are stored on the window because blender
    # doesn't seem to have any other good way of storing data
    # for quick access.
    bpy.utils.register_class(ComponentTypeData)
    bpy.utils.register_class(ComponentData)
    bpy.utils.register_class(PGSkeinWindowProps)
    bpy.types.WindowManager.skein = bpy.props.PointerProperty(type=PGSkeinWindowProps)

    bpy.types.Object.skein = bpy.props.CollectionProperty(type=ComponentData)
    bpy.types.Object.active_component_index = bpy.props.IntProperty(
        update=update_component_form
    )

    # TODO: move this to common property group for all object, material, mesh, etc extras
    bpy.types.WindowManager.selected_component = bpy.props.StringProperty(
        name="component type path",
        description="The component that will be added if selected",
        update=on_select_new_component
    )
    # skein_property_groups is a dict keyed by component type_path
    # each type_path's value is a PropertyGroup that we can introspect
    # via __annotations__ to build the UI
    bpy.types.WindowManager.skein_property_groups = {}

    # operations
    bpy.utils.register_class(FetchBevyTypeRegistry)
    bpy.utils.register_class(InsertBevyComponent)
    # panel
    bpy.utils.register_class(SkeinPanel)
    # adds the menu_func layout to an existing menu
    bpy.types.TOPBAR_MT_edit.append(menu_func)
    print("\nregister/end")

def unregister():
    # data types that are stored on the window because blender
    # doesn't seem to have any other good way of storing data
    # for quick access.
    bpy.utils.unregister_class(PGSkeinWindowProps)
    bpy.utils.unregister_class(ComponentTypeData)
    bpy.utils.unregister_class(ComponentData)
    # operations
    bpy.utils.unregister_class(FetchBevyTypeRegistry)
    bpy.utils.unregister_class(InsertBevyComponent)
    # panel
    bpy.utils.unregister_class(SkeinPanel)

# This is for testing, which allows running this script directly from Blender's Text editor
# It enables running this script without installing
if __name__ == "__main__":
    register()


# the registry is the full bevy reflection information
# the component_key is the first key into the registry, "event_ordering::PowerLevel" here:
#
# ```json
#   "event_ordering::PowerLevel": {
#     "additionalProperties": false,
#     "crateName": "event_ordering",
#     "kind": "Struct",
#     "modulePath": "event_ordering",
#     "properties": {
#       "name": {
#         "type": {
#           "$ref": "#/$defs/f32"
#         }
#       }
#     },
#     "reflectTypes": [
#       "Component",
#       "Serialize",
#       "Deserialize"
#     ],
#     "required": [
#       "name"
#     ],
#     "shortPath": "PowerLevel",
#     "type": "object",
#     "typePath": "event_ordering::PowerLevel"
#   },
# ```
def component_to_ui(registry, component_key):
    match registry[component_key]["kind"]:
        case "Array":
            return
        case "Enum":
            return
        case "List":
            return
        case "Map":
            return
        case "Set":
            return
        case "Struct":
            return
        case "Tuple":
            return
        case "TupleStruct":
            return
        case "Value":
            return
        # If an exact match is not confirmed, this last case will be used if provided
        case _:
            return "Something's wrong with the world"


# 'BoolProperty'
# 'BoolVectorProperty'
# 'CollectionProperty'
# 'EnumProperty'
# 'FloatProperty'
# 'FloatVectorProperty'
# 'IntProperty'
# 'IntVectorProperty'
# 'PointerProperty'
# 'RemoveProperty'
# 'StringProperty'

# def build_ui(registry, type) {
#     match type:
#     case ""
#     IntProperty
# }

def inc(x):
    return x + 1


def cap(val):
  return val.capitalize()
# def pascal_case(type_path):
#     type_path.join(word.capitalize() for word in s.split('::'))
def capitalize_path(s):
    return "".join(map(cap, re.split('[:_]+', s)))

# build a subclass of ComponentData which will yield PropertyGroups
# that we can build up when we fetch the registry,
# then build automatic UI from
def make_property(skein_property_groups, registry, type_path):
    type_path = type_path.removeprefix("#/$defs/")
    component = registry[type_path]
    print("\nmake_property::", type_path)
    annotations = {}

    match component["kind"]:
        case "Array":
            return
        case "Enum":
            print("Enum: ", component["type"])
            match component["type"]:
                case "string":
                    items = []
                    for item in component["oneOf"]:
                        items.append((item, item, ""))

                    print(items)

                    skein_property_groups[type_path] = bpy.props.EnumProperty(
                        items=items,
                        update=update_component_data
                    )

                    return skein_property_groups[type_path]
                case "object":
                    print("Enum.object is unimplemented")
                case _:
                    print("unknown Enum type")
                    return
        case "List":
            return
        case "Map":
            return
        case "Set":
            return
        case "Struct":
            # only recurse if we have properties to set, otherwise
            # annotations should be an empty object
            if "properties" in component:
                for key in component["properties"]:
                    print("- key: ", key)
                    annotations[key] = make_property(
                        skein_property_groups,
                        registry,
                        component["properties"][key]["type"]["$ref"]
                    )

            skein_property_groups[type_path] = type(capitalize_path(type_path), (ComponentData,), {
                '__annotations__': annotations,
            })

            return skein_property_groups[type_path]
        case "Tuple":
            return
        case "TupleStruct":
            return
        case "Value":
            print("- component[type]:  ", component["type"])
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
                case _:
                    print("unhandled: ", component["type"])
            return
        # If an exact match is not confirmed, this last case will be used if provided
        case _:
            return "Something's wrong with the world"
    # print("component", component)
    # print("annotations:\n", annotations)
    