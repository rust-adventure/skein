import bpy
import requests
import json
import re
import inspect
import os
from bpy.app.handlers import persistent # type: ignore
from .operators.insert_bevy_component import InsertBevyComponent
from .operators.fetch_bevy_type_registry import FetchBevyTypeRegistry, brp_fetch_registry_schema, process_registry
from .property_groups import ComponentData
from .skein_panel import SkeinPanel
from .operators.debug_check_object_bevy_components import DebugCheckObjectBevyComponents

# glTF extensions are named following a convention with known prefixes.
# See: https://github.com/KhronosGroup/glTF/tree/main/extensions#about-gltf-extensions
# also: https://github.com/KhronosGroup/glTF/blob/main/extensions/Prefixes.md
glTF_extension_name = "EXT_skein"

# is this extension required to view the glTF?
extension_is_required = False

# gltf exporter extension
#
# The extension takes the data from the format we need to use inside of Blender
# which can include arbitrary "active_index" selections for lists, etc and
# rewrites the skein data into a format bevy can parse and reflect directly.
#
# exported gltf extras output will look like this:
#
# ```json
# "extras":{
#   "skein":[{
#     "test_project::Rotate":{
#       "speed":1.0
#     }
#   }],
# },
# ```
class SkeinExtensionProperties(bpy.types.PropertyGroup):
    enabled: bpy.props.BoolProperty(
        name="skein",
        description='Rewrite Skein data into a directly Bevy reflectable format',
        default=True
        ) # type: ignore

# Draw the Skein settings options in the glTF export panel
def draw_export(context, layout):

    # Note: If you are using Collection Exporter, you may want to restrict UI for some collections
    # You can access the collection like this: context.collection
    # So you can check if you want to show the UI for this collection or not, using
    # if context.collection.name != "Coll":
    #     return

    header, body = layout.panel("GLTF_addon_example_exporter", default_closed=False)

    # TODO: True or False here (and in panels)? Affects visual layout
    header.use_property_split = False

    props = bpy.context.scene.skein_extension_properties

    header.prop(props, 'enabled')
    # if body != None:
    #     body.prop(props, 'float_property', text="Some float value")


# Note: the class must have this exact name
class glTF2ExportUserExtension:
    def pre_export_hook(self, export_settings):
        print("pre_export_hook in class", export_settings)

    def __init__(self):
        print("initgltf2 export user extension")
        # We need to wait until we create the gltf2UserExtension to import the gltf2 modules
        # Otherwise, it may fail because the gltf2 may not be loaded yet
        from io_scene_gltf2.io.com.gltf2_io_extensions import Extension # type: ignore
        self.Extension = Extension
        self.properties = bpy.context.scene.skein_extension_properties

    def gather_node_hook(self, gltf2_object, blender_object, export_settings):
        print("gather_node_hook")
        # Note: If you are using Collection Exporters, you may want to restrict the export for some collections
        # You can access the collection like this: export_settings['gltf_collection']
        # So you can check if you want to use this hook for this collection or not, using
        # if export_settings['gltf_collection'] != "Coll":
        #     return

        # TODO: can we report needing custom_properties enabled
        # self.report() doesn't seem available here?
        if self.properties.enabled and "skein" in gltf2_object.extras:
            print("--")
            print(gltf2_object.extras)
            print("--")
            objs = []
            for node in gltf2_object.extras["skein"]:
                obj = {}
                type_path = node["type_path"]
                obj[type_path] = node["value"]
                objs.append(obj)
            gltf2_object.extras["skein"] = objs
            
            # if gltf2_object.extensions is None:
            #     gltf2_object.extensions = {}
            # gltf2_object.extensions[glTF_extension_name] = self.Extension(
            #     name=glTF_extension_name,
            #     # extension={"float": self.properties.float_property},
            #     extension={"float": 2.0},
            #     required=extension_is_required
            # )

    def glTF2_pre_export_callback(export_settings):
        print("This will be called before exporting the glTF file.2")

    def glTF2_post_export_callback(export_settings):
        print("This will be called after exporting the glTF file.")

def pre_export_hook(self, export_settings):
    print("pre_export_hook", export_settings)
def glTF2_pre_export_callback(export_settings):
    print("idk2")
# /end gltf exporter extension

class ComponentTypeData(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name", default="Unknown") # type: ignore
    value: bpy.props.StringProperty(name="Value", default="Unknown") # type: ignore
    type_path: bpy.props.StringProperty(name="Type Path", default="Unknown") # type: ignore
    short_path: bpy.props.StringProperty(name="Short Path", default="Unknown") # type: ignore

class PGSkeinWindowProps(bpy.types.PropertyGroup):
    registry: bpy.props.StringProperty(name="Bevy Registry", default="{}") # type: ignore
    components: bpy.props.CollectionProperty(type=ComponentTypeData) # type: ignore

def update_component_form(self, context):
    """Executed when the currently selected active_component_index is changed"""
    print("\n## update component form")
    obj = context.object
    obj_skein = obj["skein"]
    active_component_index = obj.active_component_index
    global_skein = context.window_manager.skein
    registry = json.loads(global_skein.registry)
    skein_property_groups = context.window_manager.skein_property_groups
    active_component = obj_skein[active_component_index]
    type_path = active_component["type_path"]

    print("- type_path: " + type_path)

    # active_component.__dict__["value"] = bpy.props.StringProperty(default="hello")
    # print(skein_property_groups[type_path])
    # print(skein_property_groups[type_path].__annotations__)
    # TODO: What happens when we get data from object
    # and insert it
    # print("isclass", inspect.isclass(skein_property_groups[type_path]), skein_property_groups[type_path])

    if inspect.isclass(skein_property_groups[type_path]):
        bpy.types.WindowManager.active_editor = bpy.props.PointerProperty(
            type=skein_property_groups[type_path],
        )

        # TODO: get data from custom properties
        # TODO: set up recursive/nested forms
        # component_fields = inspect.get_annotations(skein_property_groups[type_path])
        # print("-- component_fields:")
        # for key, value in component_fields.items():

        #     # if key not in bpy.types.WindowManager.active_editor:
        #     #     print("next key not in active_editor; this usually means its a PropertyGroup class and not a primitive")
        #     print("   - " + key)
        #     print(registry[type_path])
        #     registry_component_data = registry[type_path]
        #     # We kind of already know this is a Struct because its an inspect.isclass from earlier
        #     if registry_component_data["kind"] == "Struct":
        #         # TODO: switch on registry[type_path]'s type
        #         field_type_path = registry[type_path]["properties"][key]["type"]["$ref"].removeprefix("#/$defs/")


                # if inspect.isclass(skein_property_groups[field_type_path]):
                # #     print("isclass")
                # #     print(value)
                # #     # print(getattr(bpy.types.WindowManager.active_editor, key))
                # #     # print(context.window_manager.active_editor.team)
                # #     # print(context.window_manager.active_editor)
                # #     # print(context.window_manager.active_editor.player)
                #     context.window_manager.active_editor[key] = bpy.props.PointerProperty(
                #         type=skein_property_groups[field_type_path],
                #     )
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
#  a hook to run when opening a     #
#  new blend file                   #
# --------------------------------- #

@persistent
def on_post_blend_file_load(blend_file):
    """blend file is empty if its the startup scene"""
    if blend_file:
        # find the location of the registry file
        registry_file = bpy.path.abspath(os.path.join("//", "skein-registry.json"))

        # try to read the schema in via skein-registry.json file if its available
        # if its not, try to use http, if http doesn't work, do nothing or report an error or something
        try:
            # read the file and try to parse it
            with open(registry_file, "r") as infile:
                content = infile.read()
                registry = json.loads(content)
                process_registry(bpy.context, registry)
        except FileNotFoundError:
            brp_response = brp_fetch_registry_schema()
            process_registry(bpy.context, brp_response["result"])
            registry_filepath = bpy.path.abspath(os.path.join("//", "skein-registry.json"))

            with open(registry_filepath,"w") as outfile:
                json.dump(brp_response["result"], outfile)

# --------------------------------- #
#  Registration and unregistration  #
# --------------------------------- #

# add to the Blender menus
def menu_func(self, context):
    self.layout.operator(FetchBevyTypeRegistry.bl_idname)
    self.layout.operator(DebugCheckObjectBevyComponents.bl_idname)

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
    bpy.utils.register_class(DebugCheckObjectBevyComponents)
    # panel
    bpy.utils.register_class(SkeinPanel)
    # adds the menu_func layout to an existing menu
    bpy.types.TOPBAR_MT_edit.append(menu_func)

    # gltf extension
    bpy.utils.register_class(SkeinExtensionProperties)
    bpy.types.Scene.skein_extension_properties = bpy.props.PointerProperty(type=SkeinExtensionProperties)

    # add handlers to run when .blend file loads
    bpy.app.handlers.load_post.append(on_post_blend_file_load)
        
    # Use the following 2 lines to register the UI for the gltf extension hook
    from io_scene_gltf2 import exporter_extension_layout_draw # type: ignore
    exporter_extension_layout_draw['Example glTF Extension'] = draw_export # Make sure to use the same name in unregister()
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
    bpy.utils.unregister_class(DebugCheckObjectBevyComponents)
    # panel
    bpy.utils.unregister_class(SkeinPanel)

    # gltf extension
    bpy.utils.unregister_class(SkeinExtensionProperties)
    del bpy.types.Scene.skein_extension_properties

    # Use the following 2 lines to unregister the UI for this hook
    from io_scene_gltf2 import exporter_extension_layout_draw # type: ignore
    del exporter_extension_layout_draw['Example glTF Extension'] # Make sure to use the same name in register()

# This is for testing, which allows running this script directly from Blender's Text editor
# It enables running this script without installing
if __name__ == "__main__":
    register()