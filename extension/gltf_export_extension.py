import inspect
import bpy

from .property_groups import hash_over_64
from .form_to_object import get_data_from_active_editor

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
    def __init__(self):
        # We need to wait until we create the gltf2UserExtension to import the gltf2 modules
        # Otherwise, it may fail because the gltf2 may not be loaded yet
        from io_scene_gltf2.io.com.gltf2_io_extensions import Extension # type: ignore
        self.Extension = Extension
        self.properties = bpy.context.scene.skein_extension_properties

    def gather_node_hook(self, gltf2_object, blender_object, export_settings):
        # Note: If you are using Collection Exporters, you may want to restrict the export for some collections
        # You can access the collection like this: export_settings['gltf_collection']
        # So you can check if you want to use this hook for this collection or not, using
        # if export_settings['gltf_collection'] != "Coll":
        #     return

        # self.report() doesn't seem available here because we aren't
        # in "Blender" we're in the "gltf2 extension"
        if self.properties.enabled:
            gather_skein_two(blender_object, gltf2_object)
            
            # if gltf2_object.extensions is None:
            #     gltf2_object.extensions = {}
            # gltf2_object.extensions[glTF_extension_name] = self.Extension(
            #     name=glTF_extension_name,
            #     # extension={"float": self.properties.float_property},
            #     extension={"float": 2.0},
            #     required=extension_is_required
            # )
    def gather_mesh_hook(self, gltf2_mesh, blender_mesh, blender_object, vertex_groups, modifiers, materials, export_settings):
        if self.properties.enabled:
            gather_skein_two(blender_mesh, gltf2_mesh)

    def gather_material_hook(self, gltf2_material, blender_material, export_settings):
        if self.properties.enabled:
            gather_skein_two(blender_material, gltf2_material)
    # gather_camera_hook(self, gltf2_camera, blender_camera, export_settings)

def glTF2_pre_export_callback(export_settings):
    print("This will be called before exporting the glTF file.")

def glTF2_post_export_callback(export_settings):
    print("This will be called after exporting the glTF file.")

def pre_export_hook(export_settings):
    pass

def gather_skein_two(source, sink):
    if "skein_two" in source:
        objs = []
        skein_property_groups = bpy.context.window_manager.skein_property_groups
        for component in source.skein_two:
            obj = {}
            type_path = component["selected_type_path"]

            if inspect.isclass(skein_property_groups[type_path]):
                try:
                    match skein_property_groups[type_path].force_default:
                        case "object":
                            obj[type_path] = {}
                        case "list":
                            obj[type_path] = []
                    objs.append(obj)
                except AttributeError:
                    value = get_data_from_active_editor(
                        component,
                        hash_over_64(type_path),
                    )
                    obj[type_path] = value
                    objs.append(obj)
            else:
                # if the component is a tuple struct, etc
                # retrieve the value directly instead of
                # recursing
                obj[type_path] = getattr(component, type_path)
                objs.append(obj)

        if sink.extras is None:
            sink.extras = {}
        sink.extras["skein"] = objs
