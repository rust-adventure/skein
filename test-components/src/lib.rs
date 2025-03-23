use bevy::prelude::*;
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

/// MultiElementTupleStruct is not currently supported in the
/// Blender addon. if you have a use case for this that isn't
/// solvable by converting to a named field struct, open an
/// issue or a PR
#[derive(Component, Reflect, Debug)]
#[reflect(Component)]
pub struct MultiElementTupleStruct(
    pub u32,
    pub Vec3,
    pub i32,
    pub String,
);

/// Marker components turn into empty object values
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
///
#[derive(Component, Reflect, Debug)]
#[reflect(Component)]
pub struct BucketOfTypes {
    /// Notably Entities can be represented by integers, but
    /// that doesn't necessarily relate to the entities in a
    /// running Bevy application
    pub entity: Entity,
    /// uuids are mostly used in Assets, which we don't really
    /// deal with inside Blender
    pub uuid: bevy::asset::uuid::Uuid,
    /// edge case-ish, but should be supportable alongside
    /// arrays
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
