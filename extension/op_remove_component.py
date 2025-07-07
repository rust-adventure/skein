import bpy

class RemoveComponentOnObject(bpy.types.Operator):
    """Remove a component on the selected object"""
    bl_idname = "object.remove_component" # unique identifier. first word is required by extensions review team to be from a specific set of words
    bl_label = "Remove Component Data (Object)" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        remove_component_data(context, context.object)
        return {'FINISHED'}

class RemoveComponentOnMesh(bpy.types.Operator):
    """Remove a component on the selected mesh"""
    bl_idname = "mesh.remove_component" # unique identifier. first word is required by extensions review team to be from a specific set of words
    bl_label = "Remove Component Data (Mesh)" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    @classmethod
    def poll(cls, context):
        return context.mesh is not None

    def execute(self, context):
        remove_component_data(context, context.mesh)
        return {'FINISHED'}

class RemoveComponentOnMaterial(bpy.types.Operator):
    """Remove a component on the selected material"""
    bl_idname = "material.remove_component" # unique identifier. first word is required by extensions review team to be from a specific set of words
    bl_label = "Remove Component Data (Material)" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    @classmethod
    def poll(cls, context):
        return context.material is not None

    def execute(self, context):
        remove_component_data(context, context.material)
        return {'FINISHED'}

class RemoveComponentOnScene(bpy.types.Operator):
    """Remove a component on the selected scene"""
    bl_idname = "scene.remove_component" # unique identifier. first word is required by extensions review team to be from a specific set of words
    bl_label = "Remove Component Data (Scene)" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    @classmethod
    def poll(cls, context):
        return context.scene is not None

    def execute(self, context):
        remove_component_data(context, context.scene)
        return {'FINISHED'}

class RemoveComponentOnLight(bpy.types.Operator):
    """Remove a component on the selected light"""
    bl_idname = "light.remove_component" # unique identifier. first word is required by extensions review team to be from a specific set of words
    bl_label = "Remove Component Data (Light)" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    @classmethod
    def poll(cls, context):
        return context.light is not None

    def execute(self, context):
        remove_component_data(context, context.light)
        return {'FINISHED'}

class RemoveComponentOnCollection(bpy.types.Operator):
    """Remove a component on the selected collection"""
    bl_idname = "collection.remove_component" # unique identifier. first word is required by extensions review team to be from a specific set of words
    bl_label = "Remove Component Data (Collection)" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    @classmethod
    def poll(cls, context):
        return context.collection is not None

    def execute(self, context):
        remove_component_data(context, context.collection)
        return {'FINISHED'}

class RemoveComponentOnBone(bpy.types.Operator):
    """Remove a component on the selected bone"""
    bl_idname = "bone.remove_component" # unique identifier. first word is required by extensions review team to be from a specific set of words
    bl_label = "Remove Component Data (Bone)" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    @classmethod
    def poll(cls, context):
        return context.bone is not None

    def execute(self, context):
        remove_component_data(context, context.bone)
        return {'FINISHED'}
    
###
def remove_component_data(context, obj):
    """
    Removing data is super generic, the only difference is where we're removing it.
    This is basically the same concept as Custom Properties which don't care what object they're on.
    """

    obj.skein_two.remove(obj.active_component_index)

    # because bpy.types.Object.active_component_index has a min=0
    # this will never be negative
    obj.active_component_index -= 1

    # blender uses strings to indicate when operation is done
    return {'FINISHED'}