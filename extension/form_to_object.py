# get json data from an active_editor
def get_data_from_active_editor(context, context_key):
    """get the data from a ComponentContainer
    The initial context is typically the ComponentContainer and the 
    typical context_key is the type_path of the Component
    """
    if context_key not in context:
        return {}
    
    # The current PropertyGroup we're working with
    obj = getattr(context, context_key)

    # get the annotations, which will give us all of the field names
    # and their value types for this PropertyGroup
    annotations = getattr(obj, "__annotations__")

    # Handle core::option::Option specially, before other enums
    # because "None" and "Some" have special meaning: null and "just the value"
    try:
        if obj.is_core_option:
            match getattr(obj, "skein_enum_index"):
                case "None":
                    return None
                case "Some":
                    if "PointerProperty" == annotations["Some"].function.__name__:
                        return get_data_from_active_editor(obj, "Some")
                    else:
                        return getattr(obj, "Some")
    except AttributeError:
        # Not all PropertyGroups have the is_core_option attribute, so
        # this is a common failure case that doesn't actually mean failure
        pass

    # If we have a `skein_enum_index`, then we have the representation
    # of a Rust Enum. The index holds the currently selected enum 
    # variant name as a string
    if "skein_enum_index" in annotations:
        match getattr(obj, "skein_enum_index"):
            # If the enum variant name doesn't exist in the fields,
            # then we have a "unit variant" and need to return
            # the variant value as a string
            case value if value not in obj:
                return value
            # return an object where the key is the enum variant name
            # and the value is the recursed value
            case value:
                if "PointerProperty" == annotations[value].function.__name__:
                    return {
                        value: get_data_from_active_editor(obj, value)
                    }
                else:
                    return { 
                        value: getattr(obj, value)
                    }

    # attempt to handle any type overrides, like glam::Vec3
    # These are mostly types where the serialization format differs from the
    # type information we get back from the Bevy type_registry.
    # For example, Vec3 is a struct and has struct reflection information
    # properly indicating that a Vec3 has x,y,z fields. BUT the serialization
    # is overridden and actually needs to be an array of 3 values
    try:
        match obj.type_override:
            case "glam::Vec3":
                return [
                    getattr(obj, "x"),
                    getattr(obj, "y"),
                    getattr(obj, "z"),
                ]
    except AttributeError:
        # Not all PropertyGroups have the type_override attribute, so
        # this is a common failure case that doesn't actually mean failure
        pass

    # No more special handling, just take the keys and values that are
    # in the annotations, and plug them into the object
    data = {}
    for key, value in annotations.items():
        if "PointerProperty" == value.function.__name__:
            data[key] = get_data_from_active_editor(obj, key)
        else:
            data[key] = getattr(obj, key)
    return data
