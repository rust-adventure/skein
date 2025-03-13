//! An example that shows the ordering of events
//!
//! 1. global `SceneInstanceReady` skein observer
//! 2. local `SceneInstanceReady` observer
//! 3. global `SkeinSceneInstanceReady` observer
//! 3. local `SkeinSceneInstanceReady` observer
//!
//! ```shell
//! ❯ RUST_LOG=info,skein=trace cargo run --example event_ordering
//! TRACE postprocess_scene: skein: global_scene_instance_ready
//!  INFO local_scene_instance_ready: event_ordering: local_scene_instance_ready
//!  INFO global_skein_scene_instance_ready: event_ordering: global_skein_scene_instance_ready
//!  INFO global_skein_scene_instance_ready: event_ordering: level=Character { name: "Hollow Knight" }
//!  INFO local_skein_scene_instance_ready: event_ordering: local_skein_scene_instance_ready
//!  INFO local_skein_scene_instance_ready: event_ordering: level=Character { name: "Hollow Knight" }
//! ```
//!
use bevy::prelude::*;
use bevy_scene::SceneInstanceReady;
use bevy_skein::{SkeinPlugin, SkeinSceneInstanceReady};
use serde::{Deserialize, Serialize};
use tracing::instrument;

fn main() {
    App::new()
        .register_type::<Character>()
        .add_plugins((
            DefaultPlugins,
            SkeinPlugin::default(),
        ))
        .add_systems(Startup, setup)
        .add_observer(global_skein_scene_instance_ready)
        .run();
}

#[instrument(skip(trigger, children, levels))]
fn local_scene_instance_ready(
    trigger: Trigger<SceneInstanceReady>,
    children: Query<&Children>,
    levels: Query<&Character>,
) {
    info!("local_scene_instance_ready");

    for entity in
        children.iter_descendants(trigger.entity())
    {
        let Ok(level) = levels.get(entity) else {
            continue;
        };
        info!(?level);
    }
}

#[instrument(skip(trigger, children, levels))]
fn global_skein_scene_instance_ready(
    trigger: Trigger<SkeinSceneInstanceReady>,
    children: Query<&Children>,
    levels: Query<&Character>,
) {
    info!("global_skein_scene_instance_ready");
    for entity in
        children.iter_descendants(trigger.entity())
    {
        let Ok(level) = levels.get(entity) else {
            continue;
        };
        info!(?level);
    }
}

#[instrument(skip(trigger, children, levels))]
fn local_skein_scene_instance_ready(
    trigger: Trigger<SkeinSceneInstanceReady>,
    children: Query<&Children>,
    levels: Query<&Character>,
) {
    info!("local_skein_scene_instance_ready");
    for entity in
        children.iter_descendants(trigger.entity())
    {
        let Ok(level) = levels.get(entity) else {
            continue;
        };
        info!(?level);
    }
}

#[derive(
    Component, Reflect, Serialize, Deserialize, Debug,
)]
#[reflect(Component, Serialize, Deserialize)]
struct Character {
    name: String,
}

fn setup(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
) {
    commands.spawn((
        Camera3d::default(),
        Transform::from_xyz(10.0, 10.0, 10.0)
            .looking_at(Vec3::ZERO, Vec3::Y),
    ));

    commands.spawn(DirectionalLight {
        shadows_enabled: true,
        ..default()
    });

    // a barebones scene containing one of each gltf_extra type
    commands
        .spawn(SceneRoot(
            asset_server.load(
                GltfAssetLabel::Scene(0)
                    .from_asset("event_ordering.gltf"),
            ),
        ))
        .observe(local_scene_instance_ready)
        .observe(local_skein_scene_instance_ready);
}
