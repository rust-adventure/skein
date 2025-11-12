import bpy # type: ignore
import json
from bpy.app.handlers import persistent
from .op_apply_preset import ApplyPresetToBone, ApplyPresetToCollection, ApplyPresetToLight, ApplyPresetToMaterial, ApplyPresetToMesh, ApplyPresetToObject, ApplyPresetToScene
from .cli_dump_component_data import dump_component_data # type: ignore
from .op_insert_component import InsertComponentOnBone, InsertComponentOnCollection, InsertComponentOnLight, InsertComponentOnMaterial, InsertComponentOnMesh, InsertComponentOnObject, InsertComponentOnScene
from .op_registry_loading import FetchRemoteTypeRegistry, ReloadSkeinRegistryJson
from .op_remove_component import RemoveComponentOnBone, RemoveComponentOnCollection, RemoveComponentOnLight, RemoveComponentOnMaterial, RemoveComponentOnMesh, RemoveComponentOnObject, RemoveComponentOnScene
from .op_debug_check_components import DebugCheckComponents
from .property_groups import ComponentData
from .skein_panel import SkeinPanelBone, SkeinPanelCollection, SkeinPanelLight, SkeinPanelObject, SkeinPanelMesh, SkeinPanelMaterial, SkeinPanelScene
from .skein_panel_presets import SkeinPanelPresetsBone, SkeinPanelPresetsCollection, SkeinPanelPresetsLight, SkeinPanelPresetsMaterial, SkeinPanelPresetsMesh, SkeinPanelPresetsObject, SkeinPanelPresetsScene # type: ignore
# these imports appear unused, but are *required* for the export extension to work
from .gltf_export_extension import glTF_extension_name, extension_is_required, SkeinExtensionProperties, draw_export, glTF2ExportUserExtension, pre_export_hook, glTF2_pre_export_callback

class SkeinAddonPreferences(bpy.types.AddonPreferences):
    # This must match the add-on name, use `__package__`
    # when defining this for add-on extensions or a sub-module of a python package.
    bl_idname = __package__

    debug: bpy.props.BoolProperty(
        name="Debug",
        description="Enable logs when launching Blender from the console",
        default=False
    ) # type: ignore
    presets: bpy.props.BoolProperty(
        name="Presets",
        description="Enable the fetching of Default and Preset implementations from Bevy, and the usage of Defaults when inserting a new Component.",
        default=True
    ) # type: ignore
    host: bpy.props.StringProperty(
        name="Host",
        description="A custom BRP host, if you configured your Bevy application with a custom BRP host.",
        default=""
    ) # type: ignore
    # port is a string so that we can take advantage of "" for "default"
    port: bpy.props.StringProperty(
        name="Port",
        description="A custom BRP port, if you configured your Bevy application with a custom BRP port.",
        default=""
    ) # type: ignore
    def draw(self, context):
        layout = self.layout
        layout.label(text="Skein Preferences")
        layout.prop(self, "debug")
        layout.prop(self, "presets")
        layout.label(text="custom host/port:")
        layout.prop(self, "host")
        layout.prop(self, "port")

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

    debug = False
    if __package__ in bpy.context.preferences.addons:
        debug = bpy.context.preferences.addons[__package__].preferences.debug

    if debug:
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
    bpy.ops.wm.reload_skein_registry()


cli_commands = []

# --------------------------------- #
#  Registration and unregistration  #
# --------------------------------- #

# add to the Blender menus
def menu_func(self, context):
    self.layout.operator(FetchRemoteTypeRegistry.bl_idname)
    # self.layout.operator(DebugCheckComponents.bl_idname)
    self.layout.operator(ReloadSkeinRegistryJson.bl_idname)

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
        min=0,
        override={"LIBRARY_OVERRIDABLE"},
    )
    bpy.types.Mesh.active_component_index = bpy.props.IntProperty(
        min=0,
        override={"LIBRARY_OVERRIDABLE"},
    )
    bpy.types.Material.active_component_index = bpy.props.IntProperty(
        min=0,
        override={"LIBRARY_OVERRIDABLE"},
    )
    bpy.types.Scene.active_component_index = bpy.props.IntProperty(
        min=0,
        override={"LIBRARY_OVERRIDABLE"},
    )
    bpy.types.Camera.active_component_index = bpy.props.IntProperty(
        min=0,
        override={"LIBRARY_OVERRIDABLE"},
    )
    bpy.types.Light.active_component_index = bpy.props.IntProperty(
        min=0,
        override={"LIBRARY_OVERRIDABLE"},
    )
    bpy.types.Collection.active_component_index = bpy.props.IntProperty(
        min=0,
        override={"LIBRARY_OVERRIDABLE"},
    )
    bpy.types.Bone.active_component_index = bpy.props.IntProperty(
        min=0,
        override={"LIBRARY_OVERRIDABLE"},
    )

    # TODO: move this to common property group for all object, material, mesh, etc extras
    bpy.types.WindowManager.selected_component = bpy.props.StringProperty(
        name="component type path",
        description="The component that will be added if selected",
        update=on_select_new_component,
    )
    # skein_property_groups is a dict keyed by component type_path
    # each type_path's value is a PropertyGroup that we can introspect
    # via __annotations__ to build the UI
    bpy.types.WindowManager.skein_property_groups = {}

    # operations
    bpy.utils.register_class(FetchRemoteTypeRegistry)
    bpy.utils.register_class(ReloadSkeinRegistryJson)
    bpy.utils.register_class(DebugCheckComponents)
    ## Insertion Operations
    bpy.utils.register_class(InsertComponentOnObject)
    bpy.utils.register_class(InsertComponentOnMesh)
    bpy.utils.register_class(InsertComponentOnMaterial)
    bpy.utils.register_class(InsertComponentOnScene)
    bpy.utils.register_class(InsertComponentOnLight)
    bpy.utils.register_class(InsertComponentOnCollection)
    bpy.utils.register_class(InsertComponentOnBone)
    ## Remove Operations
    bpy.utils.register_class(RemoveComponentOnObject)
    bpy.utils.register_class(RemoveComponentOnMesh)
    bpy.utils.register_class(RemoveComponentOnMaterial)
    bpy.utils.register_class(RemoveComponentOnScene)
    bpy.utils.register_class(RemoveComponentOnLight)
    bpy.utils.register_class(RemoveComponentOnCollection)
    bpy.utils.register_class(RemoveComponentOnBone)
    ## Preset Operations
    bpy.utils.register_class(ApplyPresetToObject)
    bpy.utils.register_class(ApplyPresetToMesh)
    bpy.utils.register_class(ApplyPresetToMaterial)
    bpy.utils.register_class(ApplyPresetToScene)
    bpy.utils.register_class(ApplyPresetToLight)
    bpy.utils.register_class(ApplyPresetToCollection)
    bpy.utils.register_class(ApplyPresetToBone)
    # panel
    bpy.utils.register_class(SkeinPanelObject)
    bpy.utils.register_class(SkeinPanelMesh)
    bpy.utils.register_class(SkeinPanelMaterial)
    bpy.utils.register_class(SkeinPanelScene)
    bpy.utils.register_class(SkeinPanelLight)
    bpy.utils.register_class(SkeinPanelCollection)
    bpy.utils.register_class(SkeinPanelBone)
    # Skein Preset Menus
    bpy.utils.register_class(SkeinPanelPresetsObject)
    bpy.utils.register_class(SkeinPanelPresetsMesh)
    bpy.utils.register_class(SkeinPanelPresetsMaterial)
    bpy.utils.register_class(SkeinPanelPresetsScene)
    bpy.utils.register_class(SkeinPanelPresetsLight)
    bpy.utils.register_class(SkeinPanelPresetsCollection)
    bpy.utils.register_class(SkeinPanelPresetsBone)
    # adds the menu_func layout to an existing menu
    bpy.types.TOPBAR_MT_edit.append(menu_func)

    # gltf extension
    bpy.utils.register_class(SkeinExtensionProperties)
    bpy.types.Scene.skein_extension_properties = bpy.props.PointerProperty(type=SkeinExtensionProperties)

    # add handlers to run when .blend file loads
    bpy.app.handlers.load_post.append(on_post_blend_file_load)

    cli_commands.append(bpy.utils.register_cli_command("dump_component_data", dump_component_data))

    # Use the following 2 lines to register the UI for the gltf extension hook
    from io_scene_gltf2 import exporter_extension_layout_draw # type: ignore
    exporter_extension_layout_draw['Example glTF Extension'] = draw_export # Make sure to use the same name in unregister()

def unregister():
    global_skein = bpy.context.window_manager.skein
    skein_property_groups = bpy.context.window_manager.skein_property_groups

    # clear the list we use as a component type selector for the UI
    global_skein.components.clear()
    # unregister all of the PropertyGroups that were created the
    # last time we processed a registry schema
    for type_path, property_group in skein_property_groups.items():
        try:
            bpy.utils.unregister_class(property_group)
        except:
            # unregister_class is recursive and we re-use classes
            # in many cases. So unregistering one class that uses 
            # another causes that class to *already* be unregistered
            # when we go to unregister it directly.
            pass

    # Clear the list that held the PropertyGroups
    skein_property_groups.clear()

    bpy.utils.unregister_class(SkeinAddonPreferences)
    # data types that are stored on the window because blender
    # doesn't seem to have any other good way of storing data
    # for quick access.
    bpy.utils.unregister_class(PGSkeinWindowProps)
    bpy.utils.unregister_class(ComponentTypeData)
    bpy.utils.unregister_class(ComponentData)
    # operations
    bpy.utils.unregister_class(FetchRemoteTypeRegistry)
    bpy.utils.unregister_class(ReloadSkeinRegistryJson)
    bpy.utils.unregister_class(DebugCheckComponents)
    ## Insertion Operations
    bpy.utils.unregister_class(InsertComponentOnObject)
    bpy.utils.unregister_class(InsertComponentOnMesh)
    bpy.utils.unregister_class(InsertComponentOnMaterial)
    bpy.utils.unregister_class(InsertComponentOnScene)
    bpy.utils.unregister_class(InsertComponentOnLight)
    bpy.utils.unregister_class(InsertComponentOnCollection)
    bpy.utils.unregister_class(InsertComponentOnBone)
    ## Remove Operations
    bpy.utils.unregister_class(RemoveComponentOnObject)
    bpy.utils.unregister_class(RemoveComponentOnMesh)
    bpy.utils.unregister_class(RemoveComponentOnMaterial)
    bpy.utils.unregister_class(RemoveComponentOnScene)
    bpy.utils.unregister_class(RemoveComponentOnLight)
    bpy.utils.unregister_class(RemoveComponentOnCollection)
    bpy.utils.unregister_class(RemoveComponentOnBone)
    ## Preset Operations
    bpy.utils.unregister_class(ApplyPresetToObject)
    bpy.utils.unregister_class(ApplyPresetToMesh)
    bpy.utils.unregister_class(ApplyPresetToMaterial)
    bpy.utils.unregister_class(ApplyPresetToScene)
    bpy.utils.unregister_class(ApplyPresetToLight)
    bpy.utils.unregister_class(ApplyPresetToCollection)
    bpy.utils.unregister_class(ApplyPresetToBone)
    # panel
    bpy.utils.unregister_class(SkeinPanelObject)
    bpy.utils.unregister_class(SkeinPanelMesh)
    bpy.utils.unregister_class(SkeinPanelMaterial)
    bpy.utils.unregister_class(SkeinPanelScene)
    bpy.utils.unregister_class(SkeinPanelLight)
    bpy.utils.unregister_class(SkeinPanelCollection)
    bpy.utils.unregister_class(SkeinPanelBone)
    # Skein Preset Menu
    bpy.utils.unregister_class(SkeinPanelPresetsObject)
    bpy.utils.unregister_class(SkeinPanelPresetsMesh)
    bpy.utils.unregister_class(SkeinPanelPresetsMaterial)
    bpy.utils.unregister_class(SkeinPanelPresetsScene)
    bpy.utils.unregister_class(SkeinPanelPresetsLight)
    bpy.utils.unregister_class(SkeinPanelPresetsCollection)
    bpy.utils.unregister_class(SkeinPanelPresetsBone)
    # gltf extension
    bpy.utils.unregister_class(SkeinExtensionProperties)
    del bpy.types.Scene.skein_extension_properties

    for cmd in cli_commands:
        bpy.utils.unregister_cli_command(cmd)
    cli_commands.clear()

    # Remove menu
    bpy.types.TOPBAR_MT_edit.remove(menu_func)

    # Use the following 2 lines to unregister the UI for this hook
    from io_scene_gltf2 import exporter_extension_layout_draw # type: ignore
    del exporter_extension_layout_draw['Example glTF Extension'] # Make sure to use the same name in register()
