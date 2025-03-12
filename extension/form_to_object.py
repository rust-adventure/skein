import inspect

# get json data from an active_editor
def get_data_from_active_editor(context, context_key, component_data, is_first_recurse):
    data = {}

    if not is_first_recurse:
        for key,value in getattr(getattr(context, context_key), "__annotations__").items():
            print(key, value)
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
                data[key] = get_data_from_active_editor(getattr(context, context_key), key, component_fields[key], False)
            else:
                data[key] = getattr(getattr(context, context_key), key)
    else:
        pass

    return data