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
use test_components::*;

fn main() {
    App::new()
        .register_type::<Player>()
        .register_type::<TeamMember>()
        .register_type::<ATupleStruct>()
        .register_type::<Marker>()
        .register_type::<TaskPriority>()
        .register_type::<SomeThings>()
        .register_type::<MultiElementTupleStruct>()
        .register_type::<AnOptionalName>()
        .register_type::<NonZeroNumbers>()
        .register_type::<AStructWithColor>()
        .register_type::<TimerContainer>()
        .register_type::<RichAndUnitEnum>()
        .register_type::<LinearVelocity>()
        .register_type::<SuperGlam>()
        // below this line are types that aren't expected to work
        .register_type::<BucketOfTypes>()
        // add plugins
        .add_plugins((
            DefaultPlugins,
            SkeinPlugin::default(),
        ))
        // .add_systems(Startup, setup)
        .run();
}

// fn setup(
//     mut commands: Commands,
//     asset_server: Res<AssetServer>,
// ) {
//     // replace this .gltf file to show data
//     commands.spawn(SceneRoot(
//         asset_server.load(
//             GltfAssetLabel::Scene(0)
//                 .from_asset("untitled.gltf"),
//         ),
//     ));
// }
