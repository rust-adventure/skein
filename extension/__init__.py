import bpy
import json
from bpy.app.handlers import persistent # type: ignore
from .operators.insert_bevy_component import InsertBevyComponent
from .operators.fetch_bevy_type_registry import FetchBevyTypeRegistry, brp_fetch_registry_schema, process_registry
from .operators.remove_bevy_component import RemoveBevyComponent
from .operators.debug_check_object_bevy_components import DebugCheckObjectBevyComponents
from .property_groups import ComponentData
from .skein_panel import SkeinPanelObject, SkeinPanelMesh, SkeinPanelMaterial
# these imports appear unused, but are *required* for the export extension to work
from .gltf_export_extension import glTF_extension_name, extension_is_required, SkeinExtensionProperties, draw_export, glTF2ExportUserExtension, pre_export_hook, glTF2_pre_export_callback

class SkeinAddonPreferences(bpy.types.AddonPreferences):
    # This must match the add-on name, use `__package__`
    # when defining this for add-on extensions or a sub-module of a python package.
    bl_idname = __name__

    debug: bpy.props.BoolProperty(
        name="Debug",
        description="Enable logs when launching Blender from the console",
        default=False
    ) # type: ignore
    def draw(self, context):
        print(__name__)
        layout = self.layout
        layout.label(text="Skein Preferences")
        layout.prop(self, "debug")

class ComponentTypeData(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name", default="Unknown") # type: ignore
    value: bpy.props.StringProperty(name="Value", default="Unknown") # type: ignore
    type_path: bpy.props.StringProperty(name="Type Path", default="Unknown") # type: ignore
    short_path: bpy.props.StringProperty(name="Short Path", default="Unknown") # type: ignore

class PGSkeinWindowProps(bpy.types.PropertyGroup):
    registry: bpy.props.StringProperty(name="Bevy Registry", default="{}") # type: ignore
    components: bpy.props.CollectionProperty(type=ComponentTypeData) # type: ignore

def on_select_new_component(self, context):
    """Executed when a new component is selected for insertion onto an object

    currently just for debugging. you can infer what fields should be shown in the ui by reading the registry data.
    """
    print("\n###### on_select_new_component")
    selected_component = context.window_manager.selected_component;
    print("\nselected_component: ", selected_component)
    global_skein = context.window_manager.skein
    if global_skein.registry:
        data = json.loads(global_skein.registry)
        if selected_component in data and len(data.keys()) > 0:
            print("\n", json.dumps(data[selected_component], indent=4))
        else:
            print("\nno data in registry")
    print("\n######\n")

# --------------------------------- #
#  a hook to run when opening a     #
#  new blend file                   #
# --------------------------------- #

@persistent
def on_post_blend_file_load(blend_file):
    """blend file is empty if its the startup scene"""
    if "skein-registry.json" in bpy.data.texts:
        # read the registry file embedded in the .blend file
        # and try to parse it
        content = bpy.data.texts["skein-registry.json"].as_string()
        registry = json.loads(content)
        process_registry(bpy.context, registry)

# --------------------------------- #
#  Registration and unregistration  #
# --------------------------------- #

# add to the Blender menus
def menu_func(self, context):
    self.layout.operator(FetchBevyTypeRegistry.bl_idname)
    self.layout.operator(DebugCheckObjectBevyComponents.bl_idname)

def register():
    bpy.utils.register_class(SkeinAddonPreferences)
    # data types that are stored on the window because blender
    # doesn't seem to have any other good way of storing data
    # for quick access.
    bpy.utils.register_class(ComponentTypeData)
    bpy.utils.register_class(ComponentData)
    bpy.utils.register_class(PGSkeinWindowProps)
    bpy.types.WindowManager.skein = bpy.props.PointerProperty(type=PGSkeinWindowProps)

    # set up per-object data types that are required to render panels
    bpy.types.Object.active_component_index = bpy.props.IntProperty(
        min=0
    )
    bpy.types.Mesh.active_component_index = bpy.props.IntProperty(
        min=0
    )
    bpy.types.Material.active_component_index = bpy.props.IntProperty(
        min=0
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
    bpy.utils.register_class(RemoveBevyComponent)
    # panel
    bpy.utils.register_class(SkeinPanelObject)
    bpy.utils.register_class(SkeinPanelMesh)
    bpy.utils.register_class(SkeinPanelMaterial)
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

def unregister():
    bpy.utils.unregister_class(SkeinAddonPreferences)
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
    bpy.utils.unregister_class(RemoveBevyComponent)
    # panel
    bpy.utils.unregister_class(SkeinPanelObject)
    bpy.utils.unregister_class(SkeinPanelMesh)
    bpy.utils.unregister_class(SkeinPanelMaterial)

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