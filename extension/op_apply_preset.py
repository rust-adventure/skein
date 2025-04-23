import json
import bpy

from .object_to_form import object_to_form
from .property_groups import hash_over_64

class ApplyPresetToObject(bpy.types.Operator):
    """Apply a preset (like Default) to the selected object"""
    bl_idname = "object.apply_preset" # unique identifier. first word is required by extensions review team to be from a specific set of words
    bl_label = "Apply Preset (Object)" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    preset_id: bpy.props.StringProperty() # type: ignore

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        apply_preset_data(context, context.object, self.preset_id)
        return {'FINISHED'}

class ApplyPresetToMesh(bpy.types.Operator):
    """Apply a preset (like Default) to the selected mesh"""
    bl_idname = "mesh.apply_preset" # unique identifier. first word is required by extensions review team to be from a specific set of words
    bl_label = "Apply Preset (Mesh)" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    preset_id: bpy.props.StringProperty() # type: ignore

    @classmethod
    def poll(cls, context):
        return context.mesh is not None

    def execute(self, context):
        apply_preset_data(context, context.mesh, self.preset_id)
        return {'FINISHED'}

class ApplyPresetToMaterial(bpy.types.Operator):
    """Apply a preset (like Default) to the selected material"""
    bl_idname = "material.apply_preset" # unique identifier. first word is required by extensions review team to be from a specific set of words
    bl_label = "Apply Preset (Material)" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    preset_id: bpy.props.StringProperty() # type: ignore

    @classmethod
    def poll(cls, context):
        return context.material is not None

    def execute(self, context):
        apply_preset_data(context, context.material, self.preset_id)
        return {'FINISHED'}
    
class ApplyPresetToLight(bpy.types.Operator):
    """Apply a preset (like Default) to the selected light"""
    bl_idname = "light.apply_preset" # unique identifier. first word is required by extensions review team to be from a specific set of words
    bl_label = "Apply Preset (Light)" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    preset_id: bpy.props.StringProperty() # type: ignore

    @classmethod
    def poll(cls, context):
        return context.light is not None

    def execute(self, context):
        apply_preset_data(context, context.light, self.preset_id)
        return {'FINISHED'}

class ApplyPresetToCollection(bpy.types.Operator):
    """Apply a preset (like Default) to the selected collection"""
    bl_idname = "collection.apply_preset" # unique identifier. first word is required by extensions review team to be from a specific set of words
    bl_label = "Apply Preset (Collection)" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    preset_id: bpy.props.StringProperty() # type: ignore

    @classmethod
    def poll(cls, context):
        return context.collection is not None

    def execute(self, context):
        apply_preset_data(context, context.collection, self.preset_id)
        return {'FINISHED'}

def apply_preset_data(context, obj, preset_id):
    """
    Inserting data is super generic, the only difference is where we're inserting it.
    This is basically the same concept as Custom Properties which don't care what object they're on.
    """
    print("preset_id: ", preset_id)
    debug = False
    presets = False
    if __package__ in bpy.context.preferences.addons:
        preferences = bpy.context.preferences.addons[__package__].preferences
        debug = preferences.debug
        presets = preferences.presets

    if debug:
        print("\napply_preset_data:")
    
    component = obj.skein_two[obj.active_component_index]

    if presets:
        try:
            if "skein-presets.json" in bpy.data.texts:
                text = bpy.data.texts["skein-presets.json"].as_string()
                embedded_presets = json.loads(text)
                print("preset info: ", embedded_presets[component.selected_type_path][preset_id])
                object_to_form(
                    component,
                    hash_over_64(component.selected_type_path),
                    embedded_presets[component.selected_type_path][preset_id]
                )
        except Exception as e:
            print("preset error: ", e)
            pass


def touch_all_fields(context, key):
    try:
        obj = getattr(context, key)
        annotations = getattr(obj, "__annotations__")
        for key, value in annotations.items():
            if "PointerProperty" == value.function.__name__:
                touch_all_fields(obj, key)
    except:
        pass