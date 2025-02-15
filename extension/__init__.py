import bpy
import requests
import json

registry_filepath = "/Users/chris/github/christopherbiscardi/skein/skein-registry.json"

class ComponentData(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name", default="Unknown")
    value: bpy.props.StringProperty(name="Value", default="Unknown")
    type_path: bpy.props.StringProperty(name="Type Path", default="Unknown")
    short_path: bpy.props.StringProperty(name="Short Path", default="Unknown")


class PGSkeinWindowProps(bpy.types.PropertyGroup):
    registry: bpy.props.StringProperty(name="Bevy Registry", default="{}")
    components: bpy.props.CollectionProperty(type=ComponentData)
    # selected_component = bpy.props.StringProperty(name="Selected Component")



def on_select_new_component(self, context):
    print("#######")
    print(context.object.name, context.window_manager.selected_component)
    print("######")

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
        # bpy.context.window_manager.skein_components_prop_search.clear()
        for k, value in brp_response["result"].items():
            if "reflectTypes" in value and "Component" in value["reflectTypes"]:
                # global_skein.components.append(k)
                component = global_skein.components.add()
                component.name = k
                component.value = k
                component.type_path = k
                component.short_path = value["shortPath"]
                # bpy.types.WindowManager.skein_components_prop_search.append(k)
                # bpy.types.WindowManager.components.append(k)
                # bpy.types.WindowManager.skein_components.append(k)
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

        # if the skein custom property doesn't exist,
        # create it.
        if "skein" not in obj.id_data:
            obj.id_data["skein"] = {};
        
        # insert a component value
        # components are unique per-entity,
        # so a dict where the keys are components makes
        # sense here
        obj.id_data["skein"]["event_ordering::Character"] = {
            "name": "Hollow Knight"
        }

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
        print("\ndraw: SkeinPanel")
        layout = self.layout
        obj = context.object
        global_skein = context.window_manager.skein


        row = layout.row()
        row.label(text="Testing Skein!", icon='WORLD_DATA')

        row = layout.row()
        row.label(text="Active object is: " + obj.name)
        row = layout.row()
        row.prop(obj, "name")
        row = layout.row()
        
        if "skein" in obj.id_data:
            print("\nSkeinPanel object custom props:")
            for key in obj.id_data["skein"].keys():
                print(key)

        # print(bpy.types.WindowManager.skein.registry)
        if global_skein.registry:
            print("\nregistry character:")
            data = json.loads(global_skein.registry)
            if len(data.keys()) > 0:
                # print(data["event_ordering::PowerLevel"])
                print(data["event_ordering::Character"])
            else:
                print("no data in registry")

        # row.prop(context.window_manager, "skein_components")
        row.prop_search(
            context.window_manager,
            'selected_component',
            global_skein,
            "components",
            text="C:"
        )
        # row.prop(context.window_manager, "skein_components_prop_search")

        # row.prop_search(bpy.types.WindowManager.skein.id_data, 'selected_component', bpy.types.WindowManager.skein, 'components')
        # row.prop(bpy.types.WindowManager.skein, "selected_component")
        # row.prop_search(bpy.types.WindowManager.skein, "selected_component", bpy.types.WindowManager.skein, "components", icon="CANCEL")
        
        # TODO: Display Component picker box

        # print(bpy.types.WindowManager.skein.registry["event_ordering::PowerLevel"])

        row = layout.row()
        row.operator("bevy.insert_bevy_component")
        print("draw/end: SkeinPanel\n")


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
    bpy.utils.register_class(ComponentData)
    bpy.utils.register_class(PGSkeinWindowProps)

    # setup global skein property group
    bpy.types.WindowManager.skein = bpy.props.PointerProperty(type=PGSkeinWindowProps)

    # test prop_search compatible data
    # bpy.types.WindowManager.skein_components_prop_search = bpy.props.PointerProperty(
    #     type=bpy.props.CollectionProperty(
    #         type=bpy.props.StringProperty(name="Component Type Path")
    #     )
    # )
    bpy.types.WindowManager.skein_components_prop_search = bpy.props.CollectionProperty(type=ComponentData)
    # bpy.types.WindowManager.skein_components_prop_search = []
    # bpy.types.WindowManager.components = bpy.types.WindowManager.skein.components

    # TODO: move this to common property group for all object, material, mesh, etc extras
    bpy.types.WindowManager.selected_component = bpy.props.StringProperty(
        name="component type path",
        description="The component that will be added if selected",
        update=on_select_new_component
    )
    #ComponentData
    # skein_components_prop_search
    # bpy.types.WindowManager.selected_component = ""


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

