import json
import bpy

from .object_to_form import object_to_form
from .property_groups import hash_over_64

class InsertComponentOnObject(bpy.types.Operator):
    """Insert a component on the selected object"""
    bl_idname = "object.insert_component" # unique identifier. first word is required by extensions review team to be from a specific set of words
    bl_label = "Insert Component Data (Object)" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        insert_component_data(context, context.object)
        return {'FINISHED'}

class InsertComponentOnMesh(bpy.types.Operator):
    """Insert a component on the selected mesh"""
    bl_idname = "mesh.insert_component" # unique identifier. first word is required by extensions review team to be from a specific set of words
    bl_label = "Insert Component Data (Mesh)" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    @classmethod
    def poll(cls, context):
        return context.mesh is not None

    def execute(self, context):
        insert_component_data(context, context.mesh)
        return {'FINISHED'}

class InsertComponentOnMaterial(bpy.types.Operator):
    """Insert a component on the selected material"""
    bl_idname = "material.insert_component" # unique identifier. first word is required by extensions review team to be from a specific set of words
    bl_label = "Insert Component Data (Material)" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    @classmethod
    def poll(cls, context):
        return context.material is not None

    def execute(self, context):
        insert_component_data(context, context.material)
        return {'FINISHED'}

class InsertComponentOnScene(bpy.types.Operator):
    """Insert a component on the selected scene"""
    bl_idname = "scene.insert_component" # unique identifier. first word is required by extensions review team to be from a specific set of words
    bl_label = "Insert Component Data (Scene)" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    @classmethod
    def poll(cls, context):
        return context.scene is not None

    def execute(self, context):
        insert_component_data(context, context.scene)
        return {'FINISHED'}
    
class InsertComponentOnLight(bpy.types.Operator):
    """Insert a component on the selected light"""
    bl_idname = "light.insert_component" # unique identifier. first word is required by extensions review team to be from a specific set of words
    bl_label = "Insert Component Data (Light)" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    @classmethod
    def poll(cls, context):
        return context.light is not None

    def execute(self, context):
        insert_component_data(context, context.light)
        return {'FINISHED'}

class InsertComponentOnCollection(bpy.types.Operator):
    """Insert a component on the selected collection"""
    bl_idname = "collection.insert_component" # unique identifier. first word is required by extensions review team to be from a specific set of words
    bl_label = "Insert Component Data (Collection)" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    @classmethod
    def poll(cls, context):
        return context.collection is not None

    def execute(self, context):
        insert_component_data(context, context.collection)
        return {'FINISHED'}

class InsertComponentOnBone(bpy.types.Operator):
    """Insert a component on the selected bone"""
    bl_idname = "bone.insert_component" # unique identifier. first word is required by extensions review team to be from a specific set of words
    bl_label = "Insert Component Data (Bone)" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    @classmethod
    def poll(cls, context):
        return context.bone is not None

    def execute(self, context):
        insert_component_data(context, context.bone)
        return {'FINISHED'}

def insert_component_data(context, obj):
    """
    Inserting data is super generic, the only difference is where we're inserting it.
    This is basically the same concept as Custom Properties which don't care what object they're on.
    """
    debug = False
    presets = False
    if __package__ in bpy.context.preferences.addons:
        preferences = bpy.context.preferences.addons[__package__].preferences
        debug = preferences.debug
        presets = preferences.presets

    if debug:
        print("\ninsert_component_data:")
    
    global_skein = context.window_manager.skein
    selected_component = context.window_manager.selected_component

    if global_skein.registry:
        registry = json.loads(global_skein.registry)
        if list(registry) and registry[selected_component]:
            data = registry[selected_component]
            if debug:
                print(data)

            new_component = obj.skein_two.add()
            new_component.name = data["shortPath"]
            new_component.selected_type_path = selected_component

            # Blender will not initialize PointerPropertys if we don't
            # access them, leading to missing data issues when we render
            # the UI. This is why we touch all PointerProperty fields
            # to make sure they're initialized.
            touch_all_fields(new_component, hash_over_64(new_component.selected_type_path))

            # If we inserted a new component, update the 
            # active_component_index to show the right editor
            # for the newly inserted component
            obj.active_component_index = len(obj.skein_two) - 1

            if presets:
                try:
                    if "skein-presets.json" in bpy.data.texts:
                        text = bpy.data.texts["skein-presets.json"].as_string()
                        embedded_presets = json.loads(text)
                        object_to_form(
                            new_component,
                            hash_over_64(new_component.selected_type_path),
                            embedded_presets[selected_component]["default"]
                        )
                except Exception as e:
                    print(e)
                    pass
        else:
            print("no data in registry")
    else:
        print("no global registry set")

def touch_all_fields(context, key):
    try:
        obj = getattr(context, key)
        annotations = getattr(obj, "__annotations__")
        for key, value in annotations.items():
            if "PointerProperty" == value.function.__name__:
                touch_all_fields(obj, key)
    except:
        pass

classes = (
    InsertComponentOnObject,
    InsertComponentOnMesh,
    InsertComponentOnMaterial,
    InsertComponentOnScene,
    InsertComponentOnLight,
    InsertComponentOnCollection,
    InsertComponentOnBone,
)

register, unregister = bpy.utils.register_classes_factory(classes)