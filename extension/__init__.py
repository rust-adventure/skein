import bpy
import json
import inspect
import os
from bpy.app.handlers import persistent # type: ignore
from .operators.insert_bevy_component import InsertBevyComponent
from .operators.fetch_bevy_type_registry import FetchBevyTypeRegistry, brp_fetch_registry_schema, process_registry
from .operators.remove_bevy_component import RemoveBevyComponent
from .operators.debug_check_object_bevy_components import DebugCheckObjectBevyComponents
from .property_groups import ComponentData
from .skein_panel import SkeinPanel
from .gltf_export_extension import glTF_extension_name, extension_is_required, SkeinExtensionProperties, draw_export, glTF2ExportUserExtension, pre_export_hook, glTF2_pre_export_callback

class ComponentTypeData(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name", default="Unknown") # type: ignore
    value: bpy.props.StringProperty(name="Value", default="Unknown") # type: ignore
    type_path: bpy.props.StringProperty(name="Type Path", default="Unknown") # type: ignore
    short_path: bpy.props.StringProperty(name="Short Path", default="Unknown") # type: ignore

class PGSkeinWindowProps(bpy.types.PropertyGroup):
    registry: bpy.props.StringProperty(name="Bevy Registry", default="{}") # type: ignore
    components: bpy.props.CollectionProperty(type=ComponentTypeData) # type: ignore

# set the active_editor form
# and pull the data from objects to fill the form if data exists
def update_component_form(self, context):
    """Executed when the currently selected active_component_index is changed"""
    print("\n## update component form")
    obj = context.object
    obj_skein = obj["skein"]
    global_skein = context.window_manager.skein
    registry = json.loads(global_skein.registry)
    skein_property_groups = context.window_manager.skein_property_groups

    # if we have a valid index
    if obj.active_component_index < len(obj_skein):
        active_component = obj_skein[obj.active_component_index]
        type_path = active_component["type_path"]

        if inspect.isclass(skein_property_groups[type_path]):
            bpy.types.WindowManager.active_editor = bpy.props.PointerProperty(
                type=skein_property_groups[type_path],
            )
            # TODO: get data from custom properties
            if "value" in active_component:
                set_form_from_data(
                    context.window_manager,
                    "active_editor",
                    active_component["value"].to_dict(),
                    skein_property_groups[type_path]
                )
        else:
            bpy.types.WindowManager.active_editor = skein_property_groups[type_path]
            if "value" in active_component:
                context.window_manager.active_editor = active_component["value"]
    else:
        bpy.types.WindowManager.active_editor = None

def set_form_from_data(context, context_key, data, component_data):
    for key, value in data.items():
        component_fields = inspect.get_annotations(component_data)
        if "skein_enum_index" in component_fields:
            setattr(getattr(context, context_key), "skein_enum_index", key)
        if isinstance(value, dict):
            component_fields = inspect.get_annotations(component_data)
            set_form_from_data(
                getattr(context, context_key),
                key,
                value,
                component_fields[key]
            )
        else:
            setattr(getattr(context, context_key), key, value)

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
        # if opening a blend file with an object that is selected
        # and has components, then show the form for the expected component
        update_component_form(None, bpy.context)

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
        update=update_component_form,
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
    bpy.utils.unregister_class(RemoveBevyComponent)
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