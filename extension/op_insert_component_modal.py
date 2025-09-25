import json
import bpy
import inspect

from .form_to_object import get_data_from_active_editor

from .op_insert_component import insert_component_data

from .skein_panel import draw_generic_panel, render_two

from .object_to_form import object_to_form
from .property_groups import hash_over_64

def get_targets(self, context):
    match self.ty:
        case "MESH":
            return [
                ("active_material","active_material",""),
            ]
        case "LIGHT":
            return [("idk","idk","")]
        case "CAMERA":
            return [("whatever","whatever","")]

        # If an exact match is not confirmed, this last case will be used if provided
        case _:
            return [("no options","no options","")]

class SelectedObjectOptions(bpy.types.PropertyGroup):
    """Options that correspond to selected objects
    """
    ty: bpy.props.StringProperty()
    targets: bpy.props.EnumProperty(
        name="target",
        items=get_targets,
        default=0
    )

class InsertComponent(bpy.types.Operator):
    """Insert Components on Selected Objects
    
    """
    bl_idname = 'wm.insert_component_modal'
    bl_label = 'Insert Components'
    bl_description ='Select objects and insert components'
    bl_options = {'REGISTER', 'UNDO'}

    selected: bpy.props.CollectionProperty(
        type=SelectedObjectOptions,
    )
    # active_component_index = bpy.props.IntProperty(
    #     min=0,
    #     override={"LIBRARY_OVERRIDABLE"},
    # )
    # ty = bpy.props.EnumProperty(
    #     name="type",
    #     items=[
    #         ("object","object","object is available"),
    #         ("mesh","mesh","mesh is available"),
    #         ("material","material","material is available")
    #     ],
    #     default="mesh"
    # )
    # skein_two = bpy.props.PointerProperty()
    # obj_file = bpy.props.StringProperty()

    def execute(self, context):
        skein_property_groups = context.window_manager.skein_property_groups

        # Iterate over all targets with a skein_two field, setting up
        # the component data for each.
        # "with a skein_two field" is controlled by the bpy.types setups
        # and the limits inflicted by the operator's enum lists
        for i, target_object in enumerate(bpy.context.selected_objects):
            user_selected_target_object = getattr(target_object, self.selected[i].targets)
            for component in context.window_manager.skein_two:
                type_path = component["selected_type_path"]
                ## create the new component, touching all PointerProperty fields
                ## with a "forced" type_path.
                insert_component_data(context, user_selected_target_object, type_path)

                target_skein_two = user_selected_target_object.skein_two
                # -1 is "last element in list"
                component_container = target_skein_two[-1]
                ## Get data from user-created component
                if inspect.isclass(skein_property_groups[type_path]):
                    data = get_data_from_active_editor(component, hash_over_64(type_path))
                    object_to_form(
                        component_container,
                        hash_over_64(type_path),
                        data
                    )
                else:
                    data = getattr(component, hash_over_64(type_path))
                    setattr(component_container, hash_over_64(type_path), data)

        self.selected.clear()
        return {'FINISHED'}

    def invoke(self, context, event):
        # self.data = {}
        # return self.execute(context)
        wm = context.window_manager
        ## clear any old skein_two data
        wm.skein_two.clear()
        for id in context.selected_ids:
            print("adding", id.type)
            select = self.selected.add()
            select.ty = id.type
        return wm.invoke_props_dialog(self, confirm_text="Insert Components")

    def draw(self, context):
        split = self.layout.row()
        col = split.column()
        for selected in self.selected:
            layout = col.column()
            layout.label(text=selected.ty)
            layout.prop(selected, "targets")
        # draw_generic_panel(context, obj, self.layout, "object", "OBJECT_PT_skein_preset_panel")
        draw_generic_panel(context, context.window_manager, split.column(), "wm", "OBJECT_PT_skein_preset_panel")



