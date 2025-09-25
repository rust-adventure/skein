# put json data into an active_editor
# This is the inverse of `form_to_object`
def object_to_form(context, context_key, data):
    """insert data into a ComponentContainer
    context is the ComponentContainer
    context_key is the type_path
    data is the component data
    """
    if context_key not in context:
         return
    
    # The current PropertyGroup we're working with
    obj = getattr(context, context_key)

    # get the annotations, which will give us all of the field names
    # and their value types for this PropertyGroup
    annotations = getattr(obj, "__annotations__")

    # Handle core::option::Option specially, before other enums
    # because "None" and "Some" have special meaning: null and "just the value"
    try:
        if obj.is_core_option:
            # if the data is a string, we have a unit variant
            # and can set the data directly
            if data is None:
                setattr(obj, "skein_enum_index", "None")
            elif isinstance(data, list) or isinstance(data, dict):
                setattr(obj, "skein_enum_index", "Some")
                object_to_form(getattr(context, context_key), "Some", data)
            else:
                setattr(obj, "skein_enum_index", "Some")
                setattr(obj, "Some", data)
            return
    except AttributeError:
        # Not all PropertyGroups have the is_core_option attribute, so
        # this is a common failure case that doesn't actually mean failure
        pass

    # If we have a `skein_enum_index`, then we have the representation
    # of a Rust Enum. The index holds the currently selected enum 
    # variant name as a string
    if "skein_enum_index" in annotations:
        # if the data is a string, we have a unit variant
        # and can set the data directly
        # TODO: should this test for all scalars? (numbers, etc)
        if isinstance(data, str):
            setattr(obj, "skein_enum_index", data)
        else:
            # otherwise we have data, and should
            # expect one key in the data object
            (enum_variant, enum_data), *rest = data.items()
            # set the skein_enum_index
            setattr(obj, "skein_enum_index", enum_variant)
            # set the key's value, if its a dict
            object_to_form(obj, enum_variant, enum_data)
            # else:
            #     print("scalar?")
            #     # setattr primitive value
            #     setattr(obj, enum_variant, enum_data)
        # if we handled an enum, return since there's 
        # no further processing to do.
        return

    # attempt to handle any type overrides, like glam::Vec3
    # These are mostly types where the serialization format differs from the
    # type information we get back from the Bevy type_registry.
    # For example, Vec3 is a struct and has struct reflection information
    # properly indicating that a Vec3 has x,y,z fields. BUT the serialization
    # is overridden and actually needs to be an array of 3 values
    try:
        print("obj.type_override", obj.type_override)
        match obj.type_override:
            case "glam::Vec2" | "glam::DVec2" | "glam::I8Vec2" | "glam::U8Vec2" | "glam::I16Vec2" | "glam::U16Vec2" | "glam::IVec2" | "glam::UVec2" | "glam::I64Vec2" | "glam::U64Vec2" | "glam::BVec2":
                return [
                    setattr(obj, "x", data[0]),
                    setattr(obj, "y", data[1]),
                ]
            case "glam::Vec3" | "glam::Vec3A" | "glam::DVec3" | "glam::I8Vec3" | "glam::U8Vec3" | "glam::I16Vec3" | "glam::U16Vec3" | "glam::IVec3" | "glam::UVec3" | "glam::I64Vec3" | "glam::U64Vec3" | "glam::BVec3":
                return [
                    setattr(obj, "x", data[0]),
                    setattr(obj, "y", data[1]),
                    setattr(obj, "z", data[2]),
                ]
            case "glam::Vec4" | "glam::DVec4" | "glam::I8Vec4" | "glam::U8Vec4" | "glam::I16Vec4" | "glam::U16Vec4" | "glam::IVec4" | "glam::UVec4" | "glam::I64Vec4" | "glam::U64Vec4" | "glam::BVec4":
                return [
                    setattr(obj, "x", data[0]),
                    setattr(obj, "y", data[1]),
                    setattr(obj, "z", data[2]),
                    setattr(obj, "w", data[3]),
                ]
            case "glam::Quat" | "glam::DQuat":
                return [
                    setattr(obj, "x", data[0]),
                    setattr(obj, "y", data[1]),
                    setattr(obj, "z", data[2]),
                    setattr(obj, "w", data[3]),
                ]
            case "glam::Mat2" | "glam::DMat2":
                x_axis = getattr(obj, "x_axis")
                y_axis = getattr(obj, "y_axis")
                
                return [
                    setattr(x_axis, "x", data[0]),
                    setattr(x_axis, "y", data[1]),

                    setattr(y_axis, "x", data[2]),
                    setattr(y_axis, "y", data[3]),
                ]

            case "glam::Mat3" | "glam::Mat3A" | "glam::DMat3":
                x_axis = getattr(obj, "x_axis")
                y_axis = getattr(obj, "y_axis")
                z_axis = getattr(obj, "z_axis")
                
                return [
                    setattr(x_axis, "x", data[0]),
                    setattr(x_axis, "y", data[1]),
                    setattr(x_axis, "z", data[2]),

                    setattr(y_axis, "x", data[3]),
                    setattr(y_axis, "y", data[4]),
                    setattr(y_axis, "z", data[5]),

                    setattr(z_axis, "x", data[6]),
                    setattr(z_axis, "y", data[7]),
                    setattr(z_axis, "z", data[8]),
                ]
            case "glam::Mat4" | "glam::DMat4":
                x_axis = getattr(obj, "x_axis")
                y_axis = getattr(obj, "y_axis")
                z_axis = getattr(obj, "z_axis")
                w_axis = getattr(obj, "w_axis")
                
                return [
                    setattr(x_axis, "x", data[0]),
                    setattr(x_axis, "y", data[1]),
                    setattr(x_axis, "z", data[2]),
                    setattr(x_axis, "w", data[3]),

                    setattr(y_axis, "x", data[4]),
                    setattr(y_axis, "y", data[5]),
                    setattr(y_axis, "z", data[6]),
                    setattr(y_axis, "w", data[7]),

                    setattr(z_axis, "x", data[8]),
                    setattr(z_axis, "y", data[9]),
                    setattr(z_axis, "z", data[10]),
                    setattr(z_axis, "w", data[11]),

                    setattr(w_axis, "x", data[12]),
                    setattr(w_axis, "y", data[13]),
                    setattr(w_axis, "z", data[14]),
                    setattr(w_axis, "w", data[15]),
                ]
  
            case "glam::Affine2" | "glam::DAffine2":
                mat = getattr(obj, "matrix2")
                x_axis = getattr(mat, "x_axis")
                y_axis = getattr(mat, "y_axis")
                translation = getattr(obj, "translation")
                
                return [
                    setattr(x_axis, "x", data[0]),
                    setattr(x_axis, "y", data[1]),
                    setattr(y_axis, "x", data[2]),
                    setattr(y_axis, "y", data[3]),
                    setattr(translation, "x", data[4]),
                    setattr(translation, "y", data[5]),
                ]
            case "glam::Affine3A" | "glam::DAffine3":
                mat = getattr(obj, "matrix3")
                x_axis = getattr(mat, "x_axis")
                y_axis = getattr(mat, "y_axis")
                z_axis = getattr(mat, "z_axis")
                translation = getattr(obj, "translation")
                
                return [
                    setattr(x_axis, "x", data[0]),
                    setattr(x_axis, "y", data[1]),
                    setattr(x_axis, "z", data[2]),
                    setattr(y_axis, "x", data[3]),
                    setattr(y_axis, "y", data[4]),
                    setattr(y_axis, "z", data[5]),
                    setattr(z_axis, "x", data[6]),
                    setattr(z_axis, "y", data[7]),
                    setattr(z_axis, "z", data[8]),
                    setattr(translation, "x", data[9]),
                    setattr(translation, "y", data[10]),
                    setattr(translation, "z", data[11]),
                ]
            
    except AttributeError:
        # Not all PropertyGroups have the type_override attribute, so
        # this is a common failure case that doesn't actually mean failure
        pass

    # No more special handling, just take the keys and values that are
    # in the annotations, and plug them into the object
    for key, value in annotations.items():
        # value is the _PropertyDeferred class here, if we need it to 
        # set values in a specific way
        if isinstance(data[key], list) or isinstance(data[key], dict) or value.function.__name__ == "PointerProperty":
            object_to_form(getattr(context, context_key), key, data[key])
        else:
            setattr(obj, key, data[key])
    return
