//! An example that shows that components are
//! added before a SceneInstanceReady is handled
use bevy::prelude::*;
use bevy_log::tracing::instrument;
use bevy_scene::SceneInstanceReady;
use bevy_skein::SkeinPlugin;
use serde::{Deserialize, Serialize};

fn main() {
    App::new()
        .add_plugins((
            DefaultPlugins,
            SkeinPlugin::default(),
        ))
        .add_systems(Startup, setup)
        .run();
}

#[instrument(skip(
    on_scene_instance_ready,
    children,
    levels
))]
fn on_scene_instance_ready(
    on_scene_instance_ready: On<SceneInstanceReady>,
    children: Query<&Children>,
    levels: Query<&Character>,
) {
    for entity in children
        .iter_descendants(on_scene_instance_ready.entity)
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

    commands
        .spawn(SceneRoot(
            asset_server.load(
                GltfAssetLabel::Scene(0)
                    .from_asset("event_ordering.gltf"),
            ),
        ))
        .observe(on_scene_instance_ready);
}
