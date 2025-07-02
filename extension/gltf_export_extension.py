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

LIGHTS = {
    "POINT": "point",
    "SUN": "directional",
    "SPOT": "spot"
}

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
            try:
                # if this is a node with a light and the KHR_lights_punctual extension is on
                # then handle the light skein data
                if blender_object.data.type in LIGHTS and "KHR_lights_punctual" in gltf2_object.extensions:
                    gather_skein_two(
                        blender_object.data,
                        gltf2_object.extensions["KHR_lights_punctual"].extension["light"].extension
                    )
            except Exception as e:
                pass

            # gather the main node skein data
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
    def gather_camera_hook(self, gltf2_camera, blender_camera, export_settings):
        if self.properties.enabled:
            gather_skein_two(blender_camera, gltf2_camera)
    def gather_joint_hook(self, gltf2_node, blender_bone, export_settings):
        # blender_bone seems to be a PoseBone
        if self.properties.enabled:
            # blender_bone.bone is the way the gltf extension grabs the extras
            # https://github.com/KhronosGroup/glTF-Blender-IO/blob/d97e93200cff331b7d58bb8347237740fd7ccd89/addons/io_scene_gltf2/blender/exp/joints.py#L119
            gather_skein_two(blender_bone.bone, gltf2_node)
        pass
    def gather_gltf_extensions_hook(self, gltf2_plan, export_settings):
        pass
    def gather_scene_hook(self, gltf2_scene, blender_scene, export_settings):
        pass
    # 
    # this commented code is some code meant to aid in debugging any
    # arbitrary feature through the export process
    # 
    # # def pre_export_hook(self, export_settings):
    # #     print("debug: ")
    # # def post_export_hook(self, export_settings):
    # #     print("debug: ")
    # def gather_animation_channel_hook(self, gltf2_animation_channel, channel, blender_object, bone, action_name, node_channel_is_animated, export_settings):
    #     print("debug: gather_animation_channel_hook")
    # def gather_animation_channel_target_hook(self, gltf2_animation_channel_target, channels, blender_object, bake_bone, bake_channel, export_settings):
    #     print("debug: gather_animation_channel_target_hook")
    # def gather_animation_sampler_hook(self, gltf2_sampler, blender_object, bone, action_name, node_channel_is_animated, export_settings):
    #     print("debug: gather_animation_sampler_hook")
    # def gather_asset_hook(self, gltf2_asset, export_settings):
    #     print("debug: gather_asset_hook")
    # # def gather_camera_hook(self, gltf2_camera, blender_camera, export_settings):
    # #     print("debug: ")
    # # def gather_gltf_extensions_hook(self, gltf2_plan, export_settings):
    # #     print("debug: ")
    # def gather_image_hook(self, gltf2_image, mapping, blender_shader_sockets, export_settings):
    #     print("debug: gather_image_hook")
    # # def gather_joint_hook(self, gltf2_node, blender_bone, export_settings):
    # #     print("debug: gather_joint_hook")
    # # def gather_material_hook(self, gltf2_material, blender_material, export_settings):
    # #     print("debug: ")
    # # def gather_material_pbr_metallic_roughness_hook(self, gltf2_material, blender_material, orm_texture, export_settings):
    # #     print("debug: ")
    # # def gather_material_unlit_hook(self, gltf2_material, blender_material, export_settings):
    # #     print("debug: ")
    # # def gather_mesh_hook(self, gltf2_mesh, blender_mesh, blender_object, vertex_groups, modifiers, materials, export_settings):
    # #     print("debug: ")
    # # def gather_node_hook(self, gltf2_node, blender_object, export_settings):
    # #     print("debug: ")
    # def gather_node_name_hook(self, gltf_name, blender_object, export_settings):
    #     print("debug: gather_node_name_hook")
    # def gather_sampler_hook(self, gltf2_sampler, blender_shader_node, export_settings):
    #     print("debug: gather_sampler_hook")
    # # def gather_scene_hook(self, gltf2_scene, blender_scene, export_settings):
    # #     print("debug: ")
    # # def gather_skin_hook(self, gltf2_skin, blender_object, export_settings):
    # #     print("debug: ")
    # def gather_texture_hook(self, gltf2_texture, blender_shader_sockets, export_settings):
    #     print("debug: gather_texture_hook")
    # def gather_texture_info_hook(self, gltf2_texture_info, blender_shader_sockets, export_settings):
    #     print("debug: gather_texture_info_hook")
    # def merge_animation_extensions_hook(self, gltf2_animation_source, gltf2_animation_destination, export_settings):
    #     print("debug: merge_animation_extensions_hook")
    # def vtree_before_filter_hook(self, vtree, export_settings):
    #     print("debug: vtree_before_filter_hook")
    # def vtree_after_filter_hook(self, vtree, export_settings):
    #     print("debug: vtree_after_filter_hook")
    # def pre_gather_animation_hook(self, gltf2_channels, blender_action, slot_identifier, blender_object, export_settings):
    #     print("debug: pre_gather_animation_hook")
    # def gather_actions_hook(self, blender_object, actions, export_settings): # params = ActionsData
    #     print("debug: gather_actions_hook")
    # def gather_tracks_hook(self, blender_object, tracks, export_settings): # params = TracksData, blender_tracks_names, track_on_type:
    #     print("debug: gather_tracks_hook")
    # def pre_gather_actions_hook(self, blender_object, export_settings): # For action mode
    #     print("debug: pre_gather_actions_hook")
    # def pre_gather_tracks_hook(self, blender_object, export_settings): # For track mode
    #     print("debug: pre_gather_tracks_hook")
    # def pre_animation_switch_hook(self, blender_object, blender_action, slot, track_name, on_type, export_settings): # For action mode:
    #     print("debug: pre_animation_switch_hook")
    # def post_animation_switch_hook(self, blender_object, blender_action, slot, track_name, on_type, export_settings):  # For action mode:
    #     print("debug: post_animation_switch_hook")
    # def pre_animation_track_switch_hook(self, blender_object, tracks, track_name, on_type, export_settings): # For track mode:
    #     print("debug: pre_animation_track_switch_hook")
    # def post_animation_track_switch_hook(self, blender_object, tracks, track_name, on_type, export_settings):  # For track mode:
    #     print("debug: post_animation_track_switch_hook")
    # def animation_switch_loop_hook(self, blender_object, post, export_settings): # post = False before loop, True after loop # for action mode:
    #     print("debug: animation_switch_loop_hook")
    # def animation_track_switch_loop_hook(self, blender_object, post, export_settings): # post = False before loop, True after loop # for track mode:
    #     print("debug: animation_track_switch_loop_hook")
    # def animation_gather_fcurve(self, blender_object, blender_action, export_settings):
    #     print("debug: animation_gather_fcurve")
    # def animation_channels_object_sampled(self, gltf2_channels, blender_object, blender_action, slot_identifier, cache_key, export_settings):
    #     print("debug: animation_channels_object_sampled")
    # def animation_gather_object_channel(self, blender_object, blender_action_name, export_settings):
    #     print("debug: animation_gather_object_channel")
    # def animation_gather_object_sampler(self, blender_object, action_name, export_settings):
    #     print("debug: animation_gather_object_sampler")
    # def animation_channels_sk_sampled(self, gltf2_channels, blender_object, blender_action, slot_identifier, cache_key, export_settings):
    #     print("debug: animation_channels_sk_sampled")
    # def animation_action_sk_sampled_target(self, blender_object, export_settings):
    #     print("debug: animation_action_sk_sampled_target")
    # def animation_gather_sk_channels(self, blender_object, blender_action_name, export_settings):
    #     print("debug: animation_gather_sk_channels")
    # def animation_gather_sk_channel(self, blender_object, blender_action_name, export_settings):
    #     print("debug: animation_gather_sk_channel")
    # def animation_gather_fcurve_channel_target(self, blender_object, bone_name, export_settings):
    #     print("debug: animation_gather_fcurve_channel_target")
    # def animation_gather_fcurve_channel_sampler(self, blender_object, bone_name, export_settings):
    #     print("debug: animation_gather_fcurve_channel_sampler")
    # def animation_gather_fcurve_channel(self, blender_object, bone_name, channel_group, export_settings):
    #     print("debug: animation_gather_fcurve_channel")
    # def gather_gltf_hook(self, active_scene_idx, scenes, animations, export_settings):
    #     print("debug: gather_gltf_hook")
    # def gather_gltf_encoded_hook(self, gltf_format, sort_order, export_settings):
    #     print("debug: gather_gltf_encoded_hook")
    # def gather_tree_filter_tag_hook(self, tree, export_settings):
    #     print("debug: gather_tree_filter_tag_hook")
    # def animation_channels_armature_sampled(self, gltf2_channels, blender_object, blender_action, slot_identifier, cache_key, export_settings):
    #     print("debug: animation_channels_armature_sampled")
    # def gather_animation_bone_sampled_channel_target_hook(self, blender_object, bone, channel, export_settings):
    #     print("debug: gather_animation_bone_sampled_channel_target_hook")
    # def gather_animation_object_sampled_channel_target_hook(self, blender_object, channel):
    #     print("debug: gather_animation_object_sampled_channel_target_hook")
    # def gather_attribute_keep(self, keep_attribute, export_settings):
    #     print("debug: gather_attribute_keep")
    # def gather_attribute_change(self, attribute, data, is_normalized_byte_color, export_settings):
    #     print("debug: gather_attribute_change")
    # def gather_attributes_change(self, attributes, export_settings):
    #     print("debug: gather_attributes_change")
    # def gather_gltf_additional_textures_hook(self, json, additioan_json_textures, export_settings):
    #     print("debug: gather_gltf_additional_textures_hook")
    # def gather_node_mesh_hook(self, option, blender_object, export_settings):
    #     print("debug: gather_node_mesh_hook")
    # def extra_animation_manage(self, extra_samplers, obj_uuid, blender_object, blender_action, gltf_channels, export_settings):
    #     print("debug: extra_animation_manage")
    # def animation_action_hook(self, gltf2_animation, blender_object, blender_action_data, export_settings):
    #     print("debug: animation_action_hook")

def glTF2_pre_export_callback(export_settings):
    print("This will be called before exporting the glTF file.")

def glTF2_post_export_callback(export_settings):
    print("This will be called after exporting the glTF file.")

def pre_export_hook(export_settings):
    pass

def gather_skein_two(source, sink):
    if "skein_two" in source:
        print("skein_two exists")
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
                obj[type_path] = getattr(component, hash_over_64(type_path))
                objs.append(obj)

        # for most items, extras is a `.` access
        # for gltf KHR lights extension (and likely other extensions?) extras is a `[]` access
        try:
            sink.extras
            if sink.extras is None:
                sink.extras = {}
            sink.extras["skein"] = objs
        except:
            if sink["extras"] is None:
                sink["extras"] = {}
            sink["extras"]["skein"] = objs

