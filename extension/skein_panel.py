import bpy
import json
import inspect

# ---------------------------------- #
#  Skein Panel for adding components #
#  This shows in the Properties      #
#  object tab.
# ---------------------------------- #

class SkeinPanel(bpy.types.Panel):
    """Creates a Panel in the Object Properties window"""
    bl_label = "Skein Bevy Panel"
    bl_idname = "OBJECT_PT_skein"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'object'

    def draw(self, context):
        layout = self.layout
        obj = context.object
        obj_skein = obj.skein
        active_component_index = obj.active_component_index
        global_skein = context.window_manager.skein
        # TODO: the registry can likely be loaded into a dict in a less
        # common place. This function runs every draw
        registry = json.loads(global_skein.registry)
        skein_property_groups = context.window_manager.skein_property_groups
        if not registry:
            layout.label(text="Bevy registry data must be loaded to work with component data")
            # TODO: show load registry
            layout.operator("bevy.fetch_type_registry")
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
            row.operator("bevy.insert_bevy_component")

        layout.label(text="Components on this object:")

        layout.template_list(
            "UI_UL_list",
            "components list",
            obj,
            "skein",
            obj,
            "active_component_index"
        )

        # build the form ui
        # obj_skein is an array of component data
        # empty lists are falsey
        if registry and obj_skein:
            active_component_data = obj_skein[active_component_index]
            layout.label(text=active_component_data["type_path"], icon='BOIDS')

            box = layout.box()
            type_path = active_component_data["type_path"]
            registry_component_reflection_data = registry[type_path]

            # Marker component
            if "properties" not in registry_component_reflection_data and registry_component_reflection_data["kind"] == "Struct":
                box.label(text="Marker components have no data to modify")
            # Other components
            if type_path in skein_property_groups:
                component_data = skein_property_groups[type_path]
                render_props(box, context.window_manager, "active_editor", component_data)
            else:
                box.label(text="No property group for " + type_path)

def render_props(layout, context, context_key, component_data):
    if context_key != "active_editor":
        for key,value in getattr(getattr(context, context_key), "__annotations__").items():
            layout.prop(getattr(context, context_key), key)

    # get the fields from the annotations in the property groups
    # we created
    component_fields = inspect.get_annotations(component_data)

    # if the context_key we're rendering is an enum with rich data
    # (aka: variants are structs), then set the fields we'll be using
    # to include the "skein_enum_index"
    if "skein_enum_index" in component_fields:
        active_enum_variant = getattr(getattr(context, context_key), "skein_enum_index")
        component_fields = {
            "skein_enum_index": component_fields["skein_enum_index"],
            active_enum_variant: component_fields[active_enum_variant]
        }

    # render ui for any fields
    if component_fields:
        # if there are component_fields, then we're dealing with a struct or enum
        for key in component_fields:
            if "PointerProperty" == component_fields[key].function.__name__:
                box = layout
                if "skein_enum_index" not in component_fields:
                    box.label(text=key + ":")
                render_props(box.box(), getattr(context, context_key), key, component_fields[key])
            else:
                layout.prop(getattr(context, context_key), key)
                if key == "skein_enum_index":
                    layout.separator(type="LINE")
    else:
        # if there aren't fields, we're dealing with a float/string/int primitive
        # and we can use .prop directly
        if context_key == "active_editor":
            layout.prop(context, context_key)
