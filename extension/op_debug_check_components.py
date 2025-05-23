import inspect
import bpy

from .property_groups import hash_over_64 # type: ignore
from .form_to_object import get_data_from_active_editor # type: ignore

class DebugCheckComponents(bpy.types.Operator):
    """Iterate over all objects and print the skein component data to console

    This can help debug storage and see what data is set for named objects
    """
    bl_idname = "wm.debug_check_components" # unique identifier. "tag" should be
    bl_label = "Check the Skein data on all objects and other IDs" # Shows up in the UI
    bl_options = {'REGISTER'}

    # execute is called to run the operator
    def execute(self, context):
        for object in bpy.data.objects:
            print("\n# ", object.name)
            print("## ", len(object.skein_two), " components:")
            for component in object.skein_two:
                print("\n----------\n### ", component.selected_type_path, "")
                skein_property_groups = context.window_manager.skein_property_groups
                if inspect.isclass(skein_property_groups[component.selected_type_path]):
                    print(get_data_from_active_editor(
                        component,
                        hash_over_64(component.selected_type_path),
                    ))
                else:
                    print(getattr(component, component.selected_type_path))
        print("-------")
        for object in bpy.data.materials:
            print("\n# ", object.name)
            print("## ", len(object.skein_two), " components:")
            for component in object.skein_two:
                print("### ", component.selected_type_path, "")
                skein_property_groups = context.window_manager.skein_property_groups
                if inspect.isclass(skein_property_groups[component.selected_type_path]):
                    print(get_data_from_active_editor(
                        component,
                        hash_over_64(component.selected_type_path),
                    ))
                else:
                    print(getattr(component, component.selected_type_path))

        return {'FINISHED'}