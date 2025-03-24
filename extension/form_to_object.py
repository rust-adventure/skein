import inspect

# get json data from an active_editor
def get_data_from_active_editor(context, context_key, component_data, is_first_recurse):
    # print("get_data_from_active_editor\n  ", context, "\n  ", context_key, "\n  ", component_data)

    # This can fail because not all PropertyGroups have the function defined as an Attribute
    try:
        # This match handles types where the serialization format differs from the
        # type information we get back from the Bevy type_registry.
        # For example, Vec3 is a struct and has struct reflection information
        # properly indicating that a Vec3 has x,y,z fields. BUT the serialization
        # is overridden and actually needs to be an array of 3 values
        match component_data.type_override:
            case "glam::Vec3":
                return [
                    getattr(getattr(context, context_key), "x"),
                    getattr(getattr(context, context_key), "y"),
                    getattr(getattr(context, context_key), "z"),
                ]
    except AttributeError:
        try: 
            obj = getattr(context, context_key)
            match obj.type_override:
                case "glam::Vec3":
                    return [
                        getattr(obj, "x"),
                        getattr(obj, "y"),
                        getattr(obj, "z"),
                    ]
        except AttributeError:
            pass
        pass
    
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
                # iterate
                case value if value not in fields:
                    return value
                case value:
                    # variant data exists
                    if "PointerProperty" == fields[value].function.__name__:
                        return {
                            value: get_data_from_active_editor(getattr(context, context_key), value, fields[value], False)
                        }
                    else:
                        return getattr(getattr(context, context_key), key)
        else:
            for key,value in fields.items():
                if "PointerProperty" == value.function.__name__:
                    data[key] = get_data_from_active_editor(getattr(context, context_key), key, value, False)
                else:
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
    if "skein_enum_index" in component_fields:
        active_enum_variant = getattr(getattr(context, context_key), "skein_enum_index")
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
            case value if value not in component_fields:
                return value
            case value:
                component_fields = {
                    value: component_fields[value]
                }

    if component_fields:
        for key in component_fields:
            if "PointerProperty" == component_fields[key].function.__name__:
                data[key] = get_data_from_active_editor(getattr(context, context_key), key, component_fields[key], False)
            else:
                data[key] = getattr(getattr(context, context_key), key)

    return data