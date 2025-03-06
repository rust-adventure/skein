import bpy

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