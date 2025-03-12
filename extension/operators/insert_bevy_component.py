import inspect
import json
import bpy

# --------------------------------- #
#  Add hardcoded test component     #
#  to object                        #
# --------------------------------- #

class InsertBevyComponent(bpy.types.Operator):
    """Insert a component on the object (for development)"""
    bl_idname = "bevy.insert_bevy_component" # unique identifier. not specially named
    bl_label = "Insert Bevy Component (Dev)" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    # this has to be set before using operator
    # op = row.operator("bevy.insert_bevy_component")
    # op.execute_mode = "object"
    execute_mode: bpy.props.EnumProperty(
        items=[("object", "object", ""), ("mesh", "mesh", ""), ("material", "material", "")],
    ) # type: ignore

    # execute is called to run the operator
    def execute(self, context):
        print("\nexecute: InsertBevyComponent")
        obj = None
        if self.execute_mode is None:
            print("execute_mode not set for InsertBevyComponent Operator, can't insert without knowing what to insert on")
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

        global_skein = context.window_manager.skein
        selected_component = context.window_manager.selected_component
        obj_skein = obj.skein

        if global_skein.registry:
            registry = json.loads(global_skein.registry)
            if list(registry) and registry[selected_component]:
                data = registry[selected_component]
                print(data)
                component = obj.skein.add()
                component.name = data["shortPath"]
                component.type_path = selected_component

                # if we're inserting a marker, there is no data to set
                # and the form never fires to update the data.
                # TODO: should we do all data insertion here?
                # The .blend file data is restored by the scene hook, but we
                # don't insert any default data unless the form is modified
                if data["kind"] == "Struct" and "properties" not in data:
                    component["value"] = {}

                component_two = obj.skein_two.add()
                component_two.name = data["shortPath"]
                component_two.selected_type_path = selected_component
                # If we inserted a new component, update the 
                # active_component_index to show the right editor
                # for the newly inserted component
                obj.active_component_index = len(obj_skein) - 1

            else:
                print("no data in registry")
        else:
            print("no global registry set")


        print("execute/end: InsertBevyComponent\n")
        # blender uses strings to indicate when operation is done
        return {'FINISHED'}