import bpy
import json

class DebugCheckObjectBevyComponents(bpy.types.Operator):
    """Iterate over all objects and print the skein component data to console

    This can help debug storage and see what data is set for named objects
    """
    bl_idname = "bevy.debug_check_object_bevy_components" # unique identifier. not specially named
    bl_label = "Check the Skein data on all objects" # Shows up in the UI
    bl_options = {'REGISTER'}

    # execute is called to run the operator
    def execute(self, context):
        for object in bpy.data.objects:
            print("\n# ", object.name)
            print("## ", len(object.skein), " components:")
            for component in object.skein:
                print("### ", component.type_path, "")
                try:
                    print(json.dumps(component["value"].to_dict(), indent=4))
                except AttributeError:
                    print(component["value"])

        return {'FINISHED'}