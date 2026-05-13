import bpy
from .property_groups import hash_over_64, PathKeyGroup


class AppendComponentListEntryOnObject(bpy.types.Operator):
    """Append a component on the selected object"""
    bl_idname = "object.append_component_list_entry" # unique identifier. first word is required by extensions review team to be from a specific set of words
    bl_label = "Append List Entry (Object)" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    path: bpy.props.CollectionProperty(type=PathKeyGroup, name="Append Path")

    @classmethod
    def poll(cls, context):
        return hasattr(context, "object") and context.object is not None

    def execute(self, context):
        append_component_list_entry_data(context, context.object, self.path)
        return {'FINISHED'}

class AppendComponentListEntryOnMesh(bpy.types.Operator):
    """Append a component on the selected mesh"""
    bl_idname = "mesh.append_component_list_entry" # unique identifier. first word is required by extensions review team to be from a specific set of words
    bl_label = "Append List Entry (Mesh)" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    path: bpy.props.CollectionProperty(type=PathKeyGroup, name="Append Path")

    @classmethod
    def poll(cls, context):
        return hasattr(context, "mesh") and context.mesh is not None

    def execute(self, context):
        append_component_list_entry_data(context, context.mesh, self.path)
        return {'FINISHED'}

class AppendComponentListEntryOnMaterial(bpy.types.Operator):
    """Append a component on the selected material"""
    bl_idname = "material.append_component_list_entry" # unique identifier. first word is required by extensions review team to be from a specific set of words
    bl_label = "Append List Entry (Material)" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    path: bpy.props.CollectionProperty(type=PathKeyGroup, name="Append Path")

    @classmethod
    def poll(cls, context):
        return hasattr(context, "material") and context.material is not None

    def execute(self, context):
        append_component_list_entry_data(context, context.material, self.path)
        return {'FINISHED'}

class AppendComponentListEntryOnScene(bpy.types.Operator):
    """Append a component on the selected scene"""
    bl_idname = "scene.append_component_list_entry" # unique identifier. first word is required by extensions review team to be from a specific set of words
    bl_label = "Append List Entry (Scene)" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    path: bpy.props.CollectionProperty(type=PathKeyGroup, name="Append Path")

    @classmethod
    def poll(cls, context):
        return hasattr(context, "scene") and context.scene is not None

    def execute(self, context):
        append_component_list_entry_data(context, context.scene, self.path)
        return {'FINISHED'}

class AppendComponentListEntryOnLight(bpy.types.Operator):
    """Append a component on the selected light"""
    bl_idname = "light.append_component_list_entry" # unique identifier. first word is required by extensions review team to be from a specific set of words
    bl_label = "Append List Entry (Light)" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    path: bpy.props.CollectionProperty(type=PathKeyGroup, name="Append Path")

    @classmethod
    def poll(cls, context):
        return hasattr(context, "light") and context.light is not None

    def execute(self, context):
        append_component_list_entry_data(context, context.light, self.path)
        return {'FINISHED'}

class AppendComponentListEntryOnCollection(bpy.types.Operator):
    """Append a component on the selected collection"""
    bl_idname = "collection.append_component_list_entry" # unique identifier. first word is required by extensions review team to be from a specific set of words
    bl_label = "Append List Entry (Collection)" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    path: bpy.props.CollectionProperty(type=PathKeyGroup, name="Append Path")

    @classmethod
    def poll(cls, context):
        return hasattr(context, "collection") and context.collection is not None

    def execute(self, context):
        append_component_list_entry_data(context, context.collection, self.path)
        return {'FINISHED'}

class AppendComponentListEntryOnBone(bpy.types.Operator):
    """Append a component on the selected bone"""
    bl_idname = "bone.append_component_list_entry" # unique identifier. first word is required by extensions review team to be from a specific set of words
    bl_label = "Append List Entry (Bone)" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    path: bpy.props.CollectionProperty(type=PathKeyGroup, name="Append Path")

    @classmethod
    def poll(cls, context):
        return hasattr(context, "bone") and context.bone is not None

    def execute(self, context):
        append_component_list_entry_data(context, context.bone, self.path)
        return {'FINISHED'}
    
###
def append_component_list_entry_data(context, obj, path):
    """
    Removing data is super generic, the only difference is where we're removing it.
    This is basically the same concept as Custom Properties which don't care what object they're on.
    """

    cur = obj.skein_two[obj.active_component_index]
    cur = getattr(cur, hash_over_64(cur.selected_type_path))
    
    for key in path:
        if key.is_index: #TODO: currently assumes only 'int' indices. 
                         # This could be extended to dicts/maps by adding more cases for the different key types
            cur = cur[int(key.value)]
        else:
            cur = getattr(cur, key.value)
    cur.add()

    # blender uses strings to indicate when operation is done
    return {'FINISHED'}

classes = (
    AppendComponentListEntryOnObject,
    AppendComponentListEntryOnMesh,
    AppendComponentListEntryOnMaterial,
    AppendComponentListEntryOnScene,
    AppendComponentListEntryOnLight,
    AppendComponentListEntryOnCollection,
    AppendComponentListEntryOnBone,
)

register, unregister = bpy.utils.register_classes_factory(classes)