//! Setting up BRP manually to change the host/port
//!
//! You will also have to configure the Blender addon
//! to look for this host/port separately
//!
//! This is a copy of the `components_on_bone` example
//! with slight modifications for BRP configuration
use std::f32::consts::PI;

use bevy::{
    color::palettes::tailwind::SLATE_950, prelude::*,
};
use bevy_skein::SkeinPlugin;

fn main() {
    App::new()
        .insert_resource(ClearColor(SLATE_950.into()))
        .add_plugins((
            DefaultPlugins
                .set(ImagePlugin::default_nearest()),
            SkeinPlugin { handle_brp: false },
            bevy_remote::RemotePlugin::default(),
            bevy_remote::http::RemoteHttpPlugin::default()
                .with_port(8000),
        ))
        .add_systems(Startup, setup)
        .add_systems(Update, control_bones)
        .run();
}

fn setup(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
) {
    // Spawn a camera in to reduce additional gltf
    // data for examples. A camera can also be
    // exported from Blender with the right export
    // settings
    commands.spawn((
        Camera3d::default(),
        Transform::from_xyz(8.0, 0., 8.0)
            .looking_at(Vec3::new(0., -1., 0.), Vec3::Y),
    ));

    commands.spawn((
        PointLight {
            shadows_enabled: true,
            ..default()
        },
        Transform::from_xyz(4.0, 8.0, 4.0),
    ));

    commands.spawn(SceneRoot(asset_server.load(
        GltfAssetLabel::Scene(0).from_asset(
            "components_on_bone/components_on_bone.gltf",
        ),
    )));
}

#[derive(Component, Reflect)]
#[reflect(Component)]
#[type_path = "components_on_bone"]
struct ControlBone;

// the bone and the cube are the same height. If we were
// rotating the cube, it would rotate around its center.
// We are rotating the Bone, which rotates from the bone's
// root instead
fn control_bones(
    mut query: Query<&mut Transform, With<ControlBone>>,
    time: Res<Time>,
) {
    for mut transform in &mut query {
        transform.rotate_x(PI * time.delta_secs());
    }
}
