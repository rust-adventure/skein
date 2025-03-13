//! An example that is only used to serve up Component
//! registry information in various ways that can be
//! tested in Blender
//!
//! it renders nothing, and only exists to serve BRP requests
//!
//! The file `./component_tests.json` is built from the BRP schema
//! this example provides and is the minimal set of types required
//! to reflect and construct values of the components registered here.
use bevy::prelude::*;
use bevy_skein::SkeinPlugin;
use serde::{Deserialize, Serialize};

fn main() {
    App::new()
        .register_type::<Player>()
        .register_type::<TeamMember>()
        .register_type::<TupleStruct>()
        .register_type::<Marker>()
        .register_type::<TaskPriority>()
        .register_type::<SomeThings>()
        .register_type::<MultiElementTupleStruct>()
        // TODO types
        .register_type::<TimerContainer>()
        .add_plugins((
            DefaultPlugins,
            SkeinPlugin::default(),
        ))
        .run();
}

#[derive(
    Component, Reflect, Serialize, Deserialize, Debug,
)]
#[reflect(Component, Serialize, Deserialize)]
struct Player {
    name: String,
    power: f32,
    test: i32,
}

#[derive(
    Component, Reflect, Serialize, Deserialize, Debug,
)]
#[reflect(Component, Serialize, Deserialize)]
struct TeamMember {
    player: Player,
    team: Team,
}

#[derive(
    Reflect, Serialize, Deserialize, Debug, Default,
)]
#[reflect(Default)]
enum Team {
    Green,
    #[default]
    Red,
    Blue,
}

#[derive(
    Component, Reflect, Serialize, Deserialize, Debug,
)]
#[reflect(Component, Serialize, Deserialize)]
struct TupleStruct(u32);

/// MultiElementTupleStruct is not currently supported in the
/// Blender addon. if you have a use case for this that isn't
/// solvable by converting to a named field struct, open an
/// issue or a PR
#[derive(
    Component, Reflect, Serialize, Deserialize, Debug,
)]
#[reflect(Component, Serialize, Deserialize)]
struct MultiElementTupleStruct(u32, Vec3, i32, String);

#[derive(
    Component, Reflect, Serialize, Deserialize, Debug,
)]
#[reflect(Component, Serialize, Deserialize)]
struct Marker;

#[derive(
    Component, Reflect, Serialize, Deserialize, Debug,
)]
#[reflect(Component, Serialize, Deserialize)]
enum TaskPriority {
    High,
    Medium,
    Low,
}

#[derive(
    Component, Reflect, Serialize, Deserialize, Debug,
)]
#[reflect(Component, Serialize, Deserialize)]
enum SomeThings {
    OneThing { name: String },
    Low(i32),
}

#[derive(Component, Reflect, Debug)]
#[reflect(Component)]
struct TimerContainer(Timer);
