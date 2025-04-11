import bpy # type: ignore
import json
import inspect

from .property_groups import hash_over_64

# ---------------------------------- #
#  Skein Panel for adding components #
#  This shows in the Properties      #
#  tabs for the relevant objects     #
# ---------------------------------- #

class SkeinPanelObject(bpy.types.Panel):
    """Creates a Panel in the Object Properties Panel for an object"""
    bl_label = "Skein Bevy Panel"
    bl_idname = "OBJECT_PT_skein"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'object'

    @classmethod
    def poll(cls, context):
        return bpy.ops.object.insert_component.poll()

    def draw(self, context):
        obj = context.object
        draw_generic_panel(context, obj, self.layout, "object")

class SkeinPanelMesh(bpy.types.Panel):
    """Creates a Panel in the Object Properties Panel for a mesh"""
    bl_label = "Skein Bevy Panel"
    bl_idname = "MESH_PT_skein"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'

    @classmethod
    def poll(cls, context):
        return bpy.ops.mesh.insert_component.poll()

    def draw(self, context):
        obj = context.mesh
        draw_generic_panel(context, obj, self.layout, "mesh")

class SkeinPanelMaterial(bpy.types.Panel):
    """Creates a Panel in the Object Properties Panel for a material"""
    bl_label = "Skein Bevy Panel"
    bl_idname = "MATERIAL_PT_skein"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'material'

    @classmethod
    def poll(cls, context):
        return bpy.ops.material.insert_component.poll()

    def draw(self, context):
        obj = context.material
        draw_generic_panel(context, obj, self.layout, "material")

class SkeinPanelLight(bpy.types.Panel):
    """Creates a Panel in the Object Properties Panel for a light"""
    bl_label = "Skein Bevy Panel"
    bl_idname = "LIGHT_PT_skein"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'

    @classmethod
    def poll(cls, context):
        return bpy.ops.light.insert_component.poll()

    def draw(self, context):
        obj = context.light
        draw_generic_panel(context, obj, self.layout, "light")

class SkeinPanelCollection(bpy.types.Panel):
    """Creates a Panel in the Object Properties Panel for a collection"""
    bl_label = "Skein Bevy Panel"
    bl_idname = "COLLECTION_PT_skein"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'collection'

    @classmethod
    def poll(cls, context):
        return bpy.ops.collection.insert_component.poll()

    def draw(self, context):
        obj = context.collection
        draw_generic_panel(context, obj, self.layout, "collection")

def draw_generic_panel(context, obj, layout, execute_mode):
        
        global_skein = context.window_manager.skein
        # TODO: the registry can likely be loaded into a dict in a less
        # common place. This function runs every draw
        registry = json.loads(global_skein.registry)
        skein_property_groups = context.window_manager.skein_property_groups

        if not registry:
            import textwrap 

            description = "The skein-registry.json text block does not exist. You can create it by fetching from a remote location or by creating the file locally."
            wrapper = textwrap.TextWrapper(width=50)
            text_lines = wrapper.wrap(text=description)
            
            for text in text_lines:
                row = layout.row(align = True)
                row.alignment = 'EXPAND'
                row.label(text=text)

            row = layout.row(align=True)
            row.operator("wm.fetch_type_registry", text="Remote")
            row.operator("wm.reload_skein_registry", text="Local")
            return

        row = layout.row()
        
        if registry:
            layout.label(text="Insert a new Component")
            box = layout.box()
            box.prop_search(
                context.window_manager,
                'selected_component',
                global_skein,
                "components",
                text="type",
                icon="BOIDS"
            )

            row = box.row()
            row.operator(execute_mode + ".insert_component")

        layout.label(text="Components on this " + execute_mode + ":")

        layout.template_list(
            "UI_UL_list",
            "components list",
            obj,
            "skein_two",
            obj,
            "active_component_index"
        )

        # build the form ui
        # obj_skein is an array of component data
        obj_skein = obj.skein_two
        if registry and obj_skein:
            active_component_data = obj_skein[obj.active_component_index]
            type_path = active_component_data.selected_type_path

            row = layout.row()
            row.label(text=active_component_data.selected_type_path, icon='BOIDS')
            row.operator(execute_mode + ".remove_component")

            if inspect.isclass(skein_property_groups[type_path]):
                if hash_over_64(type_path) not in active_component_data:
                    layout.label(text=active_component_data.name + " has no data to edit")
                else:
                    render_two(layout, active_component_data, hash_over_64(type_path))
            else:
                layout.prop(active_component_data, hash_over_64(type_path))

def render_two(layout, context, context_key):
    if context_key not in context:
        layout.label(text=context_key + " not in context")
        return
    
    # The current PropertyGroup we're working with
    obj = getattr(context, context_key)

    try:
        match obj.force_default:
            case "object":
                layout.label(text=context_key + " will be an empty object")
                return
            case "list":
                layout.label(text=context_key + " will be an empty array")
                return
    except AttributeError:
        pass

    # get the annotations, which will give us all of the field names
    # and their value types for this PropertyGroup
    annotations = getattr(obj, "__annotations__")

    # Handle core::option::Option specially, before other enums
    # because "None" and "Some" have special meaning: null and "just the value"
    try:
        if obj.is_core_option:
            layout.prop(obj, "skein_enum_index")
            match getattr(obj, "skein_enum_index"):
                case "None":
                    # layout.label(text="None")
                    pass
                case "Some":
                    layout.separator(type="LINE")
                    if "PointerProperty" == annotations["Some"].function.__name__:
                        render_two(layout, obj, "Some")
                    else:
                        layout.prop(obj, "Some")
            return
    except AttributeError as e:
        # Not all PropertyGroups have the is_core_option attribute, so
        # this is a common failure case that doesn't actually mean failure
        pass

    # If we have a `skein_enum_index`, then we have the representation
    # of a Rust Enum. The index holds the currently selected enum 
    # variant name as a string
    if "skein_enum_index" in annotations:
        layout.prop(obj, "skein_enum_index")
        layout.separator(type="LINE")
        variant = getattr(obj, "skein_enum_index")
        match variant:
            # If the enum variant name doesn't exist in the fields,
            # then we have a "unit variant" that has no data to edit
            case value if not hasattr(obj, value):#value not in obj and obj[value] is None:
                layout.label(text="Unit variants have no data to edit")
            # recurse down into the enum
            case value:
                if "PointerProperty" == annotations[value].function.__name__:
                    render_two(layout.box(), obj, value)
                else:
                    layout.prop(obj, value)
        return

    # attempt to handle any type overrides, like glam::Vec3
    # Currently all of the types here are *also* hardcoded 
    # because their serialization format differs from their
    # reflection data. That means this handling is unlikely 
    # to change. If it does, we need to ship a new version 
    # of the addon anyway.
    try:
        match obj.type_override:
            case "glam::Vec2" | "glam::DVec2" | "glam::I8Vec2" | "glam::U8Vec2" | "glam::I16Vec2" | "glam::U16Vec2" | "glam::IVec2" | "glam::UVec2" | "glam::I64Vec2" | "glam::U64Vec2" | "glam::BVec2":
                col = layout.column(align=True)
                col.label(text=context_key + ":")
                col.prop(obj, "x")
                col.prop(obj, "y")
                return
            case "glam::Vec3" | "glam::Vec3A" | "glam::DVec3" | "glam::I8Vec3" | "glam::U8Vec3" | "glam::I16Vec3" | "glam::U16Vec3" | "glam::IVec3" | "glam::UVec3" | "glam::I64Vec3" | "glam::U64Vec3" | "glam::BVec3":
                col = layout.column(align=True)
                col.label(text=context_key + ":")
                col.prop(obj, "x")
                col.prop(obj, "y")
                col.prop(obj, "z")
                return
            case "glam::Vec4" | "glam::DVec4" | "glam::I8Vec4" | "glam::U8Vec4" | "glam::I16Vec4" | "glam::U16Vec4" | "glam::IVec4" | "glam::UVec4" | "glam::I64Vec4" | "glam::U64Vec4" | "glam::BVec4":
                col = layout.column(align=True)
                col.label(text=context_key + ":")
                col.prop(obj, "x")
                col.prop(obj, "y")
                col.prop(obj, "z")
                col.prop(obj, "w")
                return
            case "glam::Quat" | "glam::DQuat":
                col = layout.column(align=True)
                col.label(text=context_key + ":")
                col.prop(obj, "x")
                col.prop(obj, "y")
                col.prop(obj, "z")
                col.prop(obj, "w")
                return
    #         case "glam::Mat2" | "glam::DMat2":
    #             x_axis = getattr(obj, "x_axis")
    #             y_axis = getattr(obj, "y_axis")
                
    #             return [
    #                 getattr(x_axis, "x"),
    #                 getattr(x_axis, "y"),

    #                 getattr(y_axis, "x"),
    #                 getattr(y_axis, "y"),
    #             ]

    #         case "glam::Mat3" | "glam::Mat3A" | "glam::DMat3":
    #             x_axis = getattr(obj, "x_axis")
    #             y_axis = getattr(obj, "y_axis")
    #             z_axis = getattr(obj, "z_axis")
                
    #             return [
    #                 getattr(x_axis, "x"),
    #                 getattr(x_axis, "y"),
    #                 getattr(x_axis, "z"),

    #                 getattr(y_axis, "x"),
    #                 getattr(y_axis, "y"),
    #                 getattr(y_axis, "z"),

    #                 getattr(z_axis, "x"),
    #                 getattr(z_axis, "y"),
    #                 getattr(z_axis, "z"),
    #             ]
    #         case "glam::Mat4" | "glam::DMat4":
    #             x_axis = getattr(obj, "x_axis")
    #             y_axis = getattr(obj, "y_axis")
    #             z_axis = getattr(obj, "z_axis")
    #             w_axis = getattr(obj, "w_axis")
                
    #             return [
    #                 getattr(x_axis, "x"),
    #                 getattr(x_axis, "y"),
    #                 getattr(x_axis, "z"),
    #                 getattr(x_axis, "w"),

    #                 getattr(y_axis, "x"),
    #                 getattr(y_axis, "y"),
    #                 getattr(y_axis, "z"),
    #                 getattr(y_axis, "w"),

    #                 getattr(z_axis, "x"),
    #                 getattr(z_axis, "y"),
    #                 getattr(z_axis, "z"),
    #                 getattr(z_axis, "w"),

    #                 getattr(w_axis, "x"),
    #                 getattr(w_axis, "y"),
    #                 getattr(w_axis, "z"),
    #                 getattr(w_axis, "w"),
    #             ]
  
    #         case "glam::Affine2" | "glam::DAffine2":
    #             mat = getattr(obj, "matrix2")
    #             x_axis = getattr(mat, "x_axis")
    #             y_axis = getattr(mat, "y_axis")
    #             translation = getattr(obj, "translation")
                
    #             return [
    #                 getattr(x_axis, "x"),
    #                 getattr(x_axis, "y"),
    #                 getattr(y_axis, "x"),
    #                 getattr(y_axis, "y"),
    #                 getattr(translation, "x"),
    #                 getattr(translation, "y"),
    #             ]
    #         case "glam::Affine3A" | "glam::DAffine3":
    #             mat = getattr(obj, "matrix3")
    #             x_axis = getattr(mat, "x_axis")
    #             y_axis = getattr(mat, "y_axis")
    #             z_axis = getattr(mat, "z_axis")
    #             translation = getattr(obj, "translation")
                
    #             return [
    #                 getattr(x_axis, "x"),
    #                 getattr(x_axis, "y"),
    #                 getattr(x_axis, "z"),
    #                 getattr(y_axis, "x"),
    #                 getattr(y_axis, "y"),
    #                 getattr(y_axis, "z"),
    #                 getattr(z_axis, "x"),
    #                 getattr(z_axis, "y"),
    #                 getattr(z_axis, "z"),
    #                 getattr(translation, "x"),
    #                 getattr(translation, "y"),
    #                 getattr(translation, "z"),
    #             ]
            
    except AttributeError:
        # Not all PropertyGroups have the type_override attribute, so
        # this is a common failure case that doesn't actually mean failure
        pass

    # No more special handling, just take the keys and values that are
    # in the annotations, and plug them into the object
    for key, value in annotations.items():
        if "PointerProperty" == value.function.__name__:
            try:
                next_type = getattr(obj, key)
                match next_type.type_override:
                    case "glam::Vec2" | "glam::DVec2" | "glam::I8Vec2" | "glam::U8Vec2" | "glam::I16Vec2" | "glam::U16Vec2" | "glam::IVec2" | "glam::UVec2" | "glam::I64Vec2" | "glam::U64Vec2" | "glam::BVec2":
                        render_two(layout, obj, key)
                    case "glam::Vec3" | "glam::Vec3A" | "glam::DVec3" | "glam::I8Vec3" | "glam::U8Vec3" | "glam::I16Vec3" | "glam::U16Vec3" | "glam::IVec3" | "glam::UVec3" | "glam::I64Vec3" | "glam::U64Vec3" | "glam::BVec3":
                        render_two(layout, obj, key)
                    case "glam::Vec4" | "glam::DVec4" | "glam::I8Vec4" | "glam::U8Vec4" | "glam::I16Vec4" | "glam::U16Vec4" | "glam::IVec4" | "glam::UVec4" | "glam::I64Vec4" | "glam::U64Vec4" | "glam::BVec4":
                        render_two(layout, obj, key)
                    case "glam::Quat" | "glam::DQuat":
                        render_two(layout, obj, key)
                    case _:
                        layout.label(text=key + ":")
                        render_two(layout.box(), obj, key)
            except AttributeError:
                layout.label(text=key + ":")
                render_two(layout.box(), obj, key)
        else:
            layout.prop(obj, key)
    return

