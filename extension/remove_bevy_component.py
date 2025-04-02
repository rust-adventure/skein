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


    # this has to be set before using operator
    # op = row.operator("bevy.insert_bevy_component")
    # op.execute_mode = "object"
    execute_mode: bpy.props.EnumProperty(
        items=[("object", "object", ""), ("mesh", "mesh", ""), ("material", "material", "")],
    ) # type: ignore

    # execute is called to run the operator
    def execute(self, context):
        obj = None
        if self.execute_mode is None:
            print("execute_mode not set for RemoveBevyComponent Operator, can't remove without knowing what to insert on")
            return {'CANCELLED'}

        match self.execute_mode:
            case "object":
                obj = context.active_object
            case "mesh":
                obj = context.mesh
            case "material":
                obj = context.material
            case _:
                # unreachable
                return {'CANCELLED'}

        obj.skein_two.remove(obj.active_component_index)

        # because bpy.types.Object.active_component_index has a min=0
        # this will never be negative
        obj.active_component_index -= 1

        # blender uses strings to indicate when operation is done
        return {'FINISHED'}