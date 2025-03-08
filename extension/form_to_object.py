import json
import inspect

# update the data on an object from a specific component
def update_component_data(self, context):
    obj_skein = context.object["skein"]
    skein_property_groups = context.window_manager.skein_property_groups
    active_component = obj_skein[context.object.active_component_index]

    if obj_skein:
        type_path = active_component["type_path"]
        
        if type_path in skein_property_groups:
            if inspect.isclass(skein_property_groups[type_path]):
                data = get_data_from_active_editor(
                    context.window_manager,
                    "active_editor",
                    skein_property_groups[type_path]
                )
                active_component["value"] = data
            else:
                active_component["value"] = context.window_manager.active_editor

# get json data from an active_editor
def get_data_from_active_editor(context, context_key, component_data):

    data = {}

    if context_key != "active_editor":
        for key,value in getattr(getattr(context, context_key), "__annotations__").items():
            data[key] = getattr(getattr(context, context_key), key)

    component_fields = inspect.get_annotations(component_data)

    # TODO: move skein_enum_index logic to exporter maybe?
    # possibly useful for moving active_form to components list
    # This `if` changes the fields that are fetched, specifically
    # so that we only export one of the variants in an enum (all variants
    # have their own key in the object)
    if "skein_enum_index" in component_fields:
        active_enum_variant = getattr(getattr(context, context_key), "skein_enum_index")
        component_fields = {
            active_enum_variant: component_fields[active_enum_variant]
        }

    if component_fields:
        for key in component_fields:
            if "PointerProperty" == component_fields[key].function.__name__:
                data[key] = get_data_from_active_editor(getattr(context, context_key), key, component_fields[key])
            else:
                data[key] = getattr(getattr(context, context_key), key)
    else:
        pass

    return data