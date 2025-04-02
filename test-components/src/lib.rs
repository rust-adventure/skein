use bevy::{math::*, prelude::*};
use std::num::{NonZeroI16, NonZeroU8};

/// A Component with fields
#[derive(Component, Reflect, Debug)]
#[reflect(Component)]
pub struct Player {
    pub name: String,
    pub power: f32,
    pub test: i32,
}

/// A Component that includes other "non-scalar"
/// types in the values
#[derive(Component, Reflect, Debug)]
#[reflect(Component)]
pub struct TeamMember {
    pub player: Player,
    pub team: Team,
}

#[derive(Reflect, Debug, Default)]
#[reflect(Default)]
pub enum Team {
    Green,
    #[default]
    Red,
    Blue,
}

/// Single-element tuple structs turn into
/// just the inner value
#[derive(Component, Reflect, Debug)]
#[reflect(Component)]
pub struct ATupleStruct(pub u32);

/// MultiElementTupleStruct is not currently
/// supported in the Blender addon. if you have a
/// use case for this that isn't solvable by
/// converting to a named field struct, open an
/// issue or a PR
#[derive(Component, Reflect, Debug)]
#[reflect(Component)]
pub struct MultiElementTupleStruct(
    pub u32,
    pub Vec3,
    pub i32,
    pub String,
);

/// Marker components turn into empty object
/// values
#[derive(Component, Reflect, Debug)]
#[reflect(Component)]
pub struct Marker;

/// An all-unit-struct enum, which
/// turns into a string like `"High"`
#[derive(Component, Reflect, Debug)]
#[reflect(Component)]
pub enum TaskPriority {
    High,
    Medium,
    Low,
}

/// a "rich" enum with a struct variant and
/// a tuple struct variant
#[derive(Component, Reflect, Debug)]
#[reflect(Component)]
pub enum SomeThings {
    OneThing { name: String },
    Low(i32),
}

/// No support for `Timer` yet
#[derive(Component, Reflect, Debug)]
#[reflect(Component)]
pub struct TimerContainer(pub Timer);

/// A Component that uses an Option,
/// which is handled specially. `Some(value)`
/// results in just the `value` and `None`
/// results in `null`
#[derive(Component, Reflect, Debug)]
#[reflect(Component)]
pub struct AnOptionalName {
    pub name: Option<String>,
}

/// A type containing a few NonZero types.
/// NonZero types are basically regular numbers
/// with "no 0 value", so we don't need to test
/// all NonZero types
#[derive(Component, Reflect, Debug)]
#[reflect(Component)]
pub struct NonZeroNumbers {
    pub small: NonZeroU8,
    pub an_int: NonZeroI16,
}

/// A selection of values that are string-ish
#[derive(Component, Reflect, Debug)]
#[reflect(Component)]
pub struct BucketOfTypes {
    /// Notably Entities can be represented by
    /// integers, but that doesn't necessarily
    /// relate to the entities in a
    /// running Bevy application
    pub entity: Entity,
    /// uuids are mostly used in Assets, which we
    /// don't really deal with inside Blender
    pub uuid: bevy::asset::uuid::Uuid,
    /// edge case-ish, but should be supportable
    /// alongside arrays
    pub bvec: BVec3A,
}

/// An enum that has a rich struct variant
/// and a unit variant
#[derive(Component, Reflect, Debug)]
#[reflect(Component)]
pub enum RichAndUnitEnum {
    Player(Player),
    NotAPlayer,
}

/// People use Color quite a bit,
/// here's a struct that uses it
#[derive(Component, Reflect, Debug)]
#[reflect(Component)]
pub struct AStructWithColor {
    pub base: Color,
    pub highlight: Color,
    // TODO: what about LinearRgba?
}

/// Avian has LinearVelocity/AngularVelocity
/// that is basically a Vec3
#[derive(Component, Reflect, Debug)]
#[reflect(Component)]
pub struct LinearVelocity(pub Vec3);

#[derive(Debug, Component, Reflect)]
#[reflect(Component)]
pub enum PlatformBehavior {
    Rotate90X,
    Rotate90Y,
    MoveLinear { start: Vec3, end: Vec3 },
}

#[derive(Component, Reflect)]
#[reflect(Component)]
pub struct SuperGlam {
    // vec2: Vec2,
    // vec3: Vec3,
    // vec4: Vec4,
    // quat: Quat, // xyzw
    // mat2: Mat2, // 4 value
    // mat3: Mat3, // 9 values
    // mat4: Mat4, // 16 values
    // affine2: bevy::math::Affine2,
    // x_axis.x
    // x_axis.y
    // y_axis.x
    // y_axis.y
    // z_axis.x
    // z_axis.y
    // affine3: bevy::math::Affine3,
    // x_axis.x
    // x_axis.y
    // x_axis.z
    // y_axis.x
    // y_axis.y
    // y_axis.z
    // z_axis.x
    // z_axis.y
    // z_axis.z
    // w_axis.x
    // w_axis.y
    // w_axis.z
    // mat2: glam::Mat2,
    vec2: Vec2,
    vec3: Vec3,
    vec3a: Vec3A,
    vec4: Vec4,
    mat2: Mat2,
    mat3: Mat3,
    mat3a: Mat3A,
    mat4: Mat4,
    quat: Quat,
    affine2: Affine2,
    affine3a: Affine3A,
    d_vec2: DVec2,
    d_vec3: DVec3,
    d_vec4: DVec4,
    d_mat2: DMat2,
    d_mat3: DMat3,
    d_mat4: DMat4,
    d_quat: DQuat,
    d_affine2: DAffine2,
    d_affine3: DAffine3,
    i8_vec2: I8Vec2,
    i8_vec3: I8Vec3,
    i8_vec4: I8Vec4,
    u8_vec2: U8Vec2,
    u8_vec3: U8Vec3,
    u8_vec4: U8Vec4,
    i16_vec2: I16Vec2,
    i16_vec3: I16Vec3,
    i16_vec4: I16Vec4,
    u16_vec2: U16Vec2,
    u16_vec3: U16Vec3,
    u16_vec4: U16Vec4,
    i_vec2: IVec2,
    i_vec3: IVec3,
    i_vec4: IVec4,
    u_vec2: UVec2,
    u_vec3: UVec3,
    u_vec4: UVec4,
    i64_vec2: I64Vec2,
    i64_vec3: I64Vec3,
    i64_vec4: I64Vec4,
    u64_vec2: U64Vec2,
    u64_vec3: U64Vec3,
    u64_vec4: U64Vec4,
    // usize vecs are in glam but not in bevy::math
    // u_size_vec2: USizeVec2,
    // u_size_vec3: USizeVec3,
    // u_size_vec4: USizeVec4,
    b_vec2: BVec2,
    b_vec3: BVec3,
    b_vec4: BVec4,
}

#[cfg(test)]
mod tests {
    use super::*;
    use bevy::{
        asset::uuid::Uuid,
        prelude::*,
        reflect::{
            GetTypeRegistration, TypeRegistry,
            serde::ReflectSerializer,
        },
    };
    use std::str::FromStr;



    fn snapshot_component_value<
        T: PartialReflect + GetTypeRegistration,
    >(
        value: &T,
        label: &str
    ) {
        let mut type_registry = TypeRegistry::new();
        type_registry.register::<T>();

        // serialize
        let serializer =
            ReflectSerializer::new(value, &type_registry);
            
        let mut settings = insta::Settings::clone_current();
        settings.set_snapshot_suffix(label);
        let _guard = settings.bind_to_scope();
       insta::assert_json_snapshot!(serializer);
    }

    #[test]
    fn struct_fields() {
        let value = Player {
            name: "Chris Biscardi".to_string(),
            power: 100.,
            test: 4,
        };

        snapshot_component_value(&value, "player");
    }

    #[test]
    fn deep_struct_fields() {
        let value = TeamMember {
            player: Player {
                name: "Chris Biscardi".to_string(),
                power: 100.,
                test: 4,
            },
            team: Team::Green,
        };

        snapshot_component_value(&value, "team_member");
    }

    #[test]
    fn tuple_struct() {
        let value = ATupleStruct(12);

        snapshot_component_value(&value, "tuple_struct");
    }

    #[test]
    fn multi_element_tuple_struct() {
        let value = MultiElementTupleStruct(
            12,
            Vec3::ZERO,
            2,
            "testing".to_string(),
        );

        snapshot_component_value(&value, "multi_element_tuple_struct");
    }

    #[test]
    fn marker_component() {
        let value = Marker;

        snapshot_component_value(&value, "marker");
    }

    #[test]
    fn enum_component() {
        let value = TaskPriority::High;

        snapshot_component_value(&value, "task_priority");
    }

    #[test]
    fn enum_component_with_fields() {
        let value = SomeThings::OneThing {
            name: "testing".to_string(),
        };

        snapshot_component_value(&value, "some_things__one_thing");
    }

    #[test]
    fn enum_component_with_fields_alt() {
        let value = SomeThings::Low(12);

        snapshot_component_value(&value, "some_things__low");
    }

    #[test]
    fn an_optional_name() {
        let value = AnOptionalName {
            name: Some("A Test Name".to_string()),
        };

        snapshot_component_value(&value, "an_optional_name__some");

        let value = AnOptionalName { name: None };
        snapshot_component_value(&value, "an_optional_name__none");
    }

    #[test]
    fn non_zero_numbers() {
        let value = NonZeroNumbers {
            small: std::num::NonZeroU8::new(255).unwrap(),
            an_int: std::num::NonZeroI16::new(-493)
                .unwrap(),
        };
        snapshot_component_value(&value, "non_zero_numbers");
    }

    #[test]
    fn bucket_of_types() {
        let value = BucketOfTypes {
            entity: Entity::PLACEHOLDER,
            // force a uuid value for testing purposes
            uuid: Uuid::from_str(
                "16c27292-862e-4555-af16-d3d8e624c6de",
            )
            .unwrap(),
            bvec: BVec3A::new(true, false, true),
        };

        snapshot_component_value(&value, "bucket_of_types");
    }

    #[test]
    fn enum_component_rich_and_unit_enum() {
        let value = RichAndUnitEnum::Player(Player {
            name: "Chris".to_string(),
            power: 10.,
            test: 42,
        });

        snapshot_component_value(&value, "rich_and_unit_enum__player");
    }

    #[test]
    fn enum_component_rich_and_unit_enum_alt() {
        let value = RichAndUnitEnum::NotAPlayer;

        snapshot_component_value(&value, "rich_and_unit_enum__not_a_player");
    }

    #[test]
    fn a_struct_with_color() {
        let value = AStructWithColor {
            base: Color::hsl(20., 50., 50.),
            highlight: Color::oklch(1., 1., 1.),
        };

        snapshot_component_value(&value, "struct_with_color");
    }

    #[test]
    fn timer_support() {
        let value = TimerContainer(Timer::from_seconds(
            2.,
            TimerMode::Once,
        ));

        snapshot_component_value(&value, "timer_container");
    }

    #[test]
    fn vec3_support() {
        let value = LinearVelocity(Vec3::splat(2.));

        snapshot_component_value(&value, "linear_velocity");
    }

    #[test]
    fn super_glam() {
        let value = SuperGlam {
            vec2: Vec2::default(),
            vec3: Vec3::default(),
            vec3a: Vec3A::default(),
            vec4: Vec4::default(),
            mat2: Mat2::default(),
            mat3: Mat3::default(),
            mat3a: Mat3A::default(),
            mat4: Mat4::default(),
            quat: Quat::default(),
            affine2: Affine2::default(),
            affine3a: Affine3A::default(),
            d_vec2: DVec2::default(),
            d_vec3: DVec3::default(),
            d_vec4: DVec4::default(),
            d_mat2: DMat2::default(),
            d_mat3: DMat3::default(),
            d_mat4: DMat4::default(),
            d_quat: DQuat::default(),
            d_affine2: DAffine2::default(),
            d_affine3: DAffine3::default(),
            i8_vec2: I8Vec2::default(),
            i8_vec3: I8Vec3::default(),
            i8_vec4: I8Vec4::default(),
            u8_vec2: U8Vec2::default(),
            u8_vec3: U8Vec3::default(),
            u8_vec4: U8Vec4::default(),
            i16_vec2: I16Vec2::default(),
            i16_vec3: I16Vec3::default(),
            i16_vec4: I16Vec4::default(),
            u16_vec2: U16Vec2::default(),
            u16_vec3: U16Vec3::default(),
            u16_vec4: U16Vec4::default(),
            i_vec2: IVec2::default(),
            i_vec3: IVec3::default(),
            i_vec4: IVec4::default(),
            u_vec2: UVec2::default(),
            u_vec3: UVec3::default(),
            u_vec4: UVec4::default(),
            i64_vec2: I64Vec2::default(),
            i64_vec3: I64Vec3::default(),
            i64_vec4: I64Vec4::default(),
            u64_vec2: U64Vec2::default(),
            u64_vec3: U64Vec3::default(),
            u64_vec4: U64Vec4::default(),
            // usize vecs are in glam but not in bevy::math
            // u_size_vec2: USizeVec2::default(),
            // u_size_vec3: USizeVec3::default(),
            // u_size_vec4: USizeVec4::default(),
            b_vec2: BVec2::default(),
            b_vec3: BVec3::default(),
            b_vec4: BVec4::default(),
        };

        snapshot_component_value(&value, "all_glam_types");
    }
}
