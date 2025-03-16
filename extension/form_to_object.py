import inspect

# get json data from an active_editor
def get_data_from_active_editor(context, context_key, component_data, is_first_recurse):
    print("get_data_from_active_editor")
    data = {}
    # print(getattr(getattr(context, context_key), "__annotations__"))
    if not is_first_recurse:
        fields = getattr(getattr(context, context_key), "__annotations__")
        if "skein_enum_index" in fields:
            active_enum_variant = getattr(getattr(context, context_key), "skein_enum_index")
            match active_enum_variant:
                # if the shortName is "None" and the fields don't include any key
                # for the "None" variant, then its pretty likely we have a core::option::Option
                case "None" if "None" not in fields:
                    return None
                # Unfortunately the same trick doesn't work for "Some".
                # Hopefully nobody names their custom enum variants "Some"
                case "Some":
                    # Some needs to return the underlying data, removing
                    # the intermediate "Some" key
                    if "PointerProperty" == fields["Some"].function.__name__:
                        return get_data_from_active_editor(getattr(context, context_key), "Some", fields["Some"], False)
                    else:
                        return getattr(getattr(context, context_key), "Some")
        else:
            for key,value in fields.items():
                print(key, value, context, context_key)
                data[key] = getattr(getattr(context, context_key), key)

    # These two ways of access annotations return different results
    # so we have to handle both?
    # getattr(getattr(context, context_key), "__annotations__")
    component_fields = inspect.get_annotations(component_data)

    # if key == "None" and "None" not in component_fields:
    #     component_fields = {
    #         "skein_enum_index": component_fields["skein_enum_index"]
    #     }
    #     pass
    # elif
    # TODO: move skein_enum_index logic to exporter maybe?
    # possibly useful for moving active_form to components list
    # This `if` changes the fields that are fetched, specifically
    # so that we only export one of the variants in an enum (all variants
    # have their own key in the object)
    print(component_fields)
    if "skein_enum_index" in component_fields:
        active_enum_variant = getattr(getattr(context, context_key), "skein_enum_index")
        print("active_enum_variant", active_enum_variant)
        match active_enum_variant:
            # if the shortName is "None" and the component_fields don't include any key
            # for the "None" variant, then its pretty likely we have a core::option::Option
            case "None" if "None" not in component_fields:
                return None
            # Unfortunately the same trick doesn't work for "Some".
            # Hopefully nobody names their custom enum variants "Some"
            case "Some":
                # Some needs to return the underlying data, removing
                # the intermediate "Some" key
                if "PointerProperty" == component_fields["Some"].function.__name__:
                    return get_data_from_active_editor(getattr(context, context_key), key, component_fields[key], False)
                else:
                    return getattr(getattr(context, context_key), key)
            case _:
                component_fields = {
                    active_enum_variant: component_fields[active_enum_variant]
                }

    if component_fields:
        for key in component_fields:
            if "PointerProperty" == component_fields[key].function.__name__:
                data[key] = get_data_from_active_editor(getattr(context, context_key), key, component_fields[key], False)
            else:
                data[key] = getattr(getattr(context, context_key), key)

    return data