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
            case "glam::Vec2" | "glam::DVec2" | "glam::I8Vec2" | "glam::U8Vec2" | "glam::I16Vec2" | "glam::U16Vec2" | "glam::IVec2" | "glam::UVec2" | "glam::I64Vec2" | "glam::U64Vec2" | "glam::BVec2":
                return [
                    getattr(obj, "x"),
                    getattr(obj, "y"),
                ]
            case "glam::Vec3" | "glam::Vec3A" | "glam::DVec3" | "glam::I8Vec3" | "glam::U8Vec3" | "glam::I16Vec3" | "glam::U16Vec3" | "glam::IVec3" | "glam::UVec3" | "glam::I64Vec3" | "glam::U64Vec3" | "glam::BVec3":
                return [
                    getattr(obj, "x"),
                    getattr(obj, "y"),
                    getattr(obj, "z"),   
                ]
            case "glam::Vec4" | "glam::DVec4" | "glam::I8Vec4" | "glam::U8Vec4" | "glam::I16Vec4" | "glam::U16Vec4" | "glam::IVec4" | "glam::UVec4" | "glam::I64Vec4" | "glam::U64Vec4" | "glam::BVec4":
                return [
                    getattr(obj, "x"),
                    getattr(obj, "y"),
                    getattr(obj, "z"),
                    getattr(obj, "w"),
                ]
            case "glam::Quat" | "glam::DQuat":
                return [
                    getattr(obj, "x"),
                    getattr(obj, "y"),
                    getattr(obj, "z"),
                    getattr(obj, "w"),
                ]
            case "glam::Mat2" | "glam::DMat2":
                x_axis = getattr(obj, "x_axis")
                y_axis = getattr(obj, "y_axis")
                
                return [
                    getattr(x_axis, "x"),
                    getattr(x_axis, "y"),

                    getattr(y_axis, "x"),
                    getattr(y_axis, "y"),
                ]

            case "glam::Mat3" | "glam::Mat3A" | "glam::DMat3":
                x_axis = getattr(obj, "x_axis")
                y_axis = getattr(obj, "y_axis")
                z_axis = getattr(obj, "z_axis")
                
                return [
                    getattr(x_axis, "x"),
                    getattr(x_axis, "y"),
                    getattr(x_axis, "z"),

                    getattr(y_axis, "x"),
                    getattr(y_axis, "y"),
                    getattr(y_axis, "z"),

                    getattr(z_axis, "x"),
                    getattr(z_axis, "y"),
                    getattr(z_axis, "z"),
                ]
            case "glam::Mat4" | "glam::DMat4":
                x_axis = getattr(obj, "x_axis")
                y_axis = getattr(obj, "y_axis")
                z_axis = getattr(obj, "z_axis")
                w_axis = getattr(obj, "w_axis")
                
                return [
                    getattr(x_axis, "x"),
                    getattr(x_axis, "y"),
                    getattr(x_axis, "z"),
                    getattr(x_axis, "w"),

                    getattr(y_axis, "x"),
                    getattr(y_axis, "y"),
                    getattr(y_axis, "z"),
                    getattr(y_axis, "w"),

                    getattr(z_axis, "x"),
                    getattr(z_axis, "y"),
                    getattr(z_axis, "z"),
                    getattr(z_axis, "w"),

                    getattr(w_axis, "x"),
                    getattr(w_axis, "y"),
                    getattr(w_axis, "z"),
                    getattr(w_axis, "w"),
                ]
  
            case "glam::Affine2" | "glam::DAffine2":
                mat = getattr(obj, "matrix2")
                x_axis = getattr(mat, "x_axis")
                y_axis = getattr(mat, "y_axis")
                translation = getattr(obj, "translation")
                
                return [
                    getattr(x_axis, "x"),
                    getattr(x_axis, "y"),
                    getattr(y_axis, "x"),
                    getattr(y_axis, "y"),
                    getattr(translation, "x"),
                    getattr(translation, "y"),
                ]
            case "glam::Affine3A" | "glam::DAffine3":
                mat = getattr(obj, "matrix3")
                x_axis = getattr(mat, "x_axis")
                y_axis = getattr(mat, "y_axis")
                z_axis = getattr(mat, "z_axis")
                translation = getattr(obj, "translation")
                
                return [
                    getattr(x_axis, "x"),
                    getattr(x_axis, "y"),
                    getattr(x_axis, "z"),
                    getattr(y_axis, "x"),
                    getattr(y_axis, "y"),
                    getattr(y_axis, "z"),
                    getattr(z_axis, "x"),
                    getattr(z_axis, "y"),
                    getattr(z_axis, "z"),
                    getattr(translation, "x"),
                    getattr(translation, "y"),
                    getattr(translation, "z"),
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
