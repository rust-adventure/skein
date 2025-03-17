import inspect
import bpy # type: ignore

from ..form_to_object import get_data_from_active_editor # type: ignore

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
            print("## ", len(object.skein_two), " components:")
            for component in object.skein_two:
                print("### ", component.selected_type_path, "")
                skein_property_groups = context.window_manager.skein_property_groups
                if inspect.isclass(skein_property_groups[component.selected_type_path]):
                    print("object:")
                    print(get_data_from_active_editor(
                        component,
                        component.selected_type_path,
                        skein_property_groups[component.selected_type_path],
                        True
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
                    print("object:")
                    print(get_data_from_active_editor(
                        component,
                        component.selected_type_path,
                        skein_property_groups[component.selected_type_path],
                        True
                    ))
                else:
                    print(getattr(component, component.selected_type_path))

        return {'FINISHED'}