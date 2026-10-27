import bpy
from .property_groups import hash_over_64, PathKeyGroup

class RemoveComponentListEntryOnObject(bpy.types.Operator):
    """Remove a component on the selected object"""
    bl_idname = "object.remove_component_list_entry" # unique identifier. first word is required by extensions review team to be from a specific set of words
    bl_label = "Remove List Entry (Object)" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    path: bpy.props.CollectionProperty(type=PathKeyGroup, name="Remove Path")

    @classmethod
    def poll(cls, context):
        return hasattr(context, "object") and context.object is not None

    def execute(self, context):
        remove_component_list_entry_data(context, context.object, self.path)
        return {'FINISHED'}

class RemoveComponentListEntryOnMesh(bpy.types.Operator):
    """Remove a component on the selected mesh"""
    bl_idname = "mesh.remove_component_list_entry" # unique identifier. first word is required by extensions review team to be from a specific set of words
    bl_label = "Remove List Entry (Mesh)" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    path: bpy.props.CollectionProperty(type=PathKeyGroup, name="Remove Path")

    @classmethod
    def poll(cls, context):
        return hasattr(context, "mesh") and context.mesh is not None

    def execute(self, context):
        remove_component_list_entry_data(context, context.mesh, self.path)
        return {'FINISHED'}

class RemoveComponentListEntryOnMaterial(bpy.types.Operator):
    """Remove a component on the selected material"""
    bl_idname = "material.remove_component_list_entry" # unique identifier. first word is required by extensions review team to be from a specific set of words
    bl_label = "Remove List Entry (Material)" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    path: bpy.props.CollectionProperty(type=PathKeyGroup, name="Remove Path")

    @classmethod
    def poll(cls, context):
        return hasattr(context, "material") and context.material is not None

    def execute(self, context):
        remove_component_list_entry_data(context, context.material, self.path)
        return {'FINISHED'}

class RemoveComponentListEntryOnScene(bpy.types.Operator):
    """Remove a component on the selected scene"""
    bl_idname = "scene.remove_component_list_entry" # unique identifier. first word is required by extensions review team to be from a specific set of words
    bl_label = "Remove List Entry (Scene)" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    path: bpy.props.CollectionProperty(type=PathKeyGroup, name="Remove Path")

    @classmethod
    def poll(cls, context):
        return hasattr(context, "scene") and context.scene is not None

    def execute(self, context):
        remove_component_list_entry_data(context, context.scene, self.path)
        return {'FINISHED'}

class RemoveComponentListEntryOnLight(bpy.types.Operator):
    """Remove a component on the selected light"""
    bl_idname = "light.remove_component_list_entry" # unique identifier. first word is required by extensions review team to be from a specific set of words
    bl_label = "Remove List Entry (Light)" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    path: bpy.props.CollectionProperty(type=PathKeyGroup, name="Remove Path")
    
    @classmethod
    def poll(cls, context):
        return hasattr(context, "light") and context.light is not None

    def execute(self, context):
        remove_component_list_entry_data(context, context.light, self.path)
        return {'FINISHED'}

class RemoveComponentListEntryOnCollection(bpy.types.Operator):
    """Remove a component on the selected collection"""
    bl_idname = "collection.remove_component_list_entry" # unique identifier. first word is required by extensions review team to be from a specific set of words
    bl_label = "Remove List Entry (Collection)" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    path: bpy.props.CollectionProperty(type=PathKeyGroup, name="Remove Path")
    
    @classmethod
    def poll(cls, context):
        return hasattr(context, "collection") and context.collection is not None

    def execute(self, context):
        remove_component_list_entry_data(context, context.collection, self.path)
        return {'FINISHED'}

class RemoveComponentListEntryOnBone(bpy.types.Operator):
    """Remove a component on the selected bone"""
    bl_idname = "bone.remove_component_list_entry" # unique identifier. first word is required by extensions review team to be from a specific set of words
    bl_label = "Remove List Entry (Bone)" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    path: bpy.props.CollectionProperty(type=PathKeyGroup, name="Remove Path")
    
    @classmethod
    def poll(cls, context):
        return hasattr(context, "bone") and context.bone is not None

    def execute(self, context):
        remove_component_list_entry_data(context, context.bone)
        return {'FINISHED'}
    
###
def remove_component_list_entry_data(context, obj, path):
    """
    Removing data is super generic, the only difference is where we're removing it.
    This is basically the same concept as Custom Properties which don't care what object they're on.
    """
    
    cur = obj.skein_two[obj.active_component_index]
    cur = getattr(cur, hash_over_64(cur.selected_type_path))
    
    for key in path[:-1]:
        if key.is_index:
            cur = cur[int(key.value)]
        else:
            cur = getattr(cur, key.value)
    cur.remove(int(path[-1].value))

    # blender uses strings to indicate when operation is done
    return {'FINISHED'}

classes = (
    RemoveComponentListEntryOnObject,
    RemoveComponentListEntryOnMesh,
    RemoveComponentListEntryOnMaterial,
    RemoveComponentListEntryOnScene,
    RemoveComponentListEntryOnLight,
    RemoveComponentListEntryOnCollection,
    RemoveComponentListEntryOnBone,
)

register, unregister = bpy.utils.register_classes_factory(classes)