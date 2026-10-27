# get json data from an active_editor
def get_data_from_active_editor(context, context_key, index = None):
    """get the data from a ComponentContainer
    The initial context is typically the ComponentContainer and the 
    typical context_key is the type_path of the Component
    """
    if context_key not in context:
        return {}

    # The current PropertyGroup we're working with
    obj = getattr(context, context_key)

    if index is not None: # traverse into arrays, lists etc. if an index is
        obj = obj[index]  # provided in addition to the context_key

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
                        return getattr(obj, "Some").inner
    except AttributeError:
        # Not all PropertyGroups have the is_core_option attribute, so
        # this is a common failure case that doesn't actually mean failure
        pass

    # Handle tuples by merging their fields into an array 
    # to match what serde json expects them to look like
    try:
        if obj.is_tuple:
            tuple_length = getattr(obj, 'tuple_length')
            data = []
            for i in range(tuple_length): 
                data.append(get_data_from_active_editor(obj, str(i)))
            return data
    except AttributeError:
        # Same as for obj.is_core_option, not having an is_tuple field is not a hard failure
        pass

    # Handle lists (and sets) by traversing into the inner 'list_wrapper'
    # CollectionProperty and gathering all values from it into a list
    try:
        if obj.is_list:
            data = []
            for i, item in enumerate(getattr(obj, "list_wrapper")):
                data.append(get_data_from_active_editor(obj, "list_wrapper", i))
            return data
    except AttributeError:
        pass

    # If we have a `skein_enum_index`, then we have the representation
    # of a Rust Enum. The index holds the currently selected enum 
    # variant name as a string
    if "skein_enum_index" in annotations:
        match getattr(obj, "skein_enum_index"):
            # If the enum variant name doesn't exist in the fields,
            # then we have a "unit variant" and need to return
            # the variant value as a string
            case value if not hasattr(obj, value):
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
                        value: getattr(obj, value).inner
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
                    getattr(obj.x, "inner"),
                    getattr(obj.y, "inner"),
                ]
            case "glam::Vec3" | "glam::Vec3A" | "glam::DVec3" | "glam::I8Vec3" | "glam::U8Vec3" | "glam::I16Vec3" | "glam::U16Vec3" | "glam::IVec3" | "glam::UVec3" | "glam::I64Vec3" | "glam::U64Vec3" | "glam::BVec3":
                return [
                    getattr(obj.x, "inner"),
                    getattr(obj.y, "inner"),
                    getattr(obj.z, "inner"),   
                ]
            case "glam::Vec4" | "glam::DVec4" | "glam::I8Vec4" | "glam::U8Vec4" | "glam::I16Vec4" | "glam::U16Vec4" | "glam::IVec4" | "glam::UVec4" | "glam::I64Vec4" | "glam::U64Vec4" | "glam::BVec4":
                return [
                    getattr(obj.x, "inner"),
                    getattr(obj.y, "inner"),
                    getattr(obj.z, "inner"),
                    getattr(obj.w, "inner"),
                ]
            case "glam::Quat" | "glam::DQuat":
                return [
                    getattr(obj.x, "inner"),
                    getattr(obj.y, "inner"),
                    getattr(obj.z, "inner"),
                    getattr(obj.w, "inner"),
                ]
            case "glam::Mat2" | "glam::DMat2":
                x_axis = getattr(obj, "x_axis")
                y_axis = getattr(obj, "y_axis")
                
                return [
                    getattr(x_axis.x, "inner"),
                    getattr(x_axis.y, "inner"),

                    getattr(y_axis.x, "inner"),
                    getattr(y_axis.y, "inner"),
                ]

            case "glam::Mat3" | "glam::Mat3A" | "glam::DMat3":
                x_axis = getattr(obj, "x_axis")
                y_axis = getattr(obj, "y_axis")
                z_axis = getattr(obj, "z_axis")
                
                return [
                    getattr(x_axis.x, "inner"),
                    getattr(x_axis.y, "inner"),
                    getattr(x_axis.z, "inner"),

                    getattr(y_axis.x, "inner"),
                    getattr(y_axis.y, "inner"),
                    getattr(y_axis.z, "inner"),

                    getattr(z_axis.x, "inner"),
                    getattr(z_axis.y, "inner"),
                    getattr(z_axis.z, "inner"),
                ]
            case "glam::Mat4" | "glam::DMat4":
                x_axis = getattr(obj, "x_axis")
                y_axis = getattr(obj, "y_axis")
                z_axis = getattr(obj, "z_axis")
                w_axis = getattr(obj, "w_axis")
                
                return [
                    getattr(x_axis.x, "inner"),
                    getattr(x_axis.y, "inner"),
                    getattr(x_axis.z, "inner"),
                    getattr(x_axis.w, "inner"),

                    getattr(y_axis.x, "inner"),
                    getattr(y_axis.y, "inner"),
                    getattr(y_axis.z, "inner"),
                    getattr(y_axis.w, "inner"),

                    getattr(z_axis.x, "inner"),
                    getattr(z_axis.y, "inner"),
                    getattr(z_axis.z, "inner"),
                    getattr(z_axis.w, "inner"),

                    getattr(w_axis.x, "inner"),
                    getattr(w_axis.y, "inner"),
                    getattr(w_axis.z, "inner"),
                    getattr(w_axis.w, "inner"),
                ]
  
            case "glam::Affine2" | "glam::DAffine2":
                mat = getattr(obj, "matrix2")
                x_axis = getattr(mat, "x_axis")
                y_axis = getattr(mat, "y_axis")
                translation = getattr(obj, "translation")
                
                return [
                    getattr(x_axis.x, "inner"),
                    getattr(x_axis.y, "inner"),
                    getattr(y_axis.x, "inner"),
                    getattr(y_axis.y, "inner"),
                    getattr(translation.x, "inner"),
                    getattr(translation.y, "inner"),
                ]
            case "glam::Affine3A" | "glam::DAffine3":
                mat = getattr(obj, "matrix3")
                x_axis = getattr(mat, "x_axis")
                y_axis = getattr(mat, "y_axis")
                z_axis = getattr(mat, "z_axis")
                translation = getattr(obj, "translation")
                
                return [
                    getattr(x_axis.x, "inner"),
                    getattr(x_axis.y, "inner"),
                    getattr(x_axis.z, "inner"),
                    getattr(y_axis.x, "inner"),
                    getattr(y_axis.y, "inner"),
                    getattr(y_axis.z, "inner"),
                    getattr(z_axis.x, "inner"),
                    getattr(z_axis.y, "inner"),
                    getattr(z_axis.z, "inner"),
                    getattr(translation.x, "inner"),
                    getattr(translation.y, "inner"),
                    getattr(translation.z, "inner"),
                ]
            
    except AttributeError:
        # Not all PropertyGroups have the type_override attribute, so
        # this is a common failure case that doesn't actually mean failure
        pass

    # if the object has a "force_default", then we're 
    # forcing an empty value. This can happen if a TupleStruct
    # contains a `force_default` type
    try:
        if obj.force_default:
            match obj.force_default:
                case "object":
                    return {}
                case "list":
                    return []
    except AttributeError:
        pass
    
    try:
        if obj.is_value:
            return obj.inner
    except AttributeError:
        pass

    # No more special handling, just take the keys and values that are
    # in the annotations, and plug them into the object
    data = {}
    for key, value in annotations.items():
        if "PointerProperty" == value.function.__name__:
            try:
                if getattr(obj, key).is_value:
                    try:
                        data[key] = getattr(obj, key).inner
                    except Exception as e:
                        pass
                    continue
            except AttributeError as e:
                pass
            data[key] = get_data_from_active_editor(obj, key)
        else:
            try:
                if getattr(obj, key).is_value:
                    data[key] = getattr(obj, key).inner
            except:
                data[key] = getattr(obj, key)
    return data
