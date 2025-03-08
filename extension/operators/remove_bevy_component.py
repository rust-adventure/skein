import json
import bpy

# --------------------------------- #
#  Add hardcoded test component     #
#  to object                        #
# --------------------------------- #

class RemoveBevyComponent(bpy.types.Operator):
    """Remove a component on the object (for development)"""
    bl_idname = "bevy.remove_bevy_component" # unique identifier. not specially named
    bl_label = "Remove Bevy Component (Dev)" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    # execute is called to run the operator
    def execute(self, context):
        obj = context.active_object

        obj.skein.remove(obj.active_component_index)

        # because bpy.types.Object.active_component_index has a min=0
        # this will never be negative
        obj.active_component_index -= 1

        # blender uses strings to indicate when operation is done
        return {'FINISHED'}