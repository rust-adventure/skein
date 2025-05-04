//! An example that mirrors bevy's gltf extras
//! example showing how gltf extras get translated
//! to components
use bevy::{
    gltf::{
        GltfExtras, GltfMaterialExtras, GltfMeshExtras,
        GltfSceneExtras,
    },
    prelude::*,
};
use bevy_scene::SceneInstanceReady;
use bevy_skein::SkeinPlugin;
use serde::{Deserialize, Serialize};

fn main() {
    App::new()
        .register_type::<PowerLevel>()
        .add_plugins((
            DefaultPlugins,
            SkeinPlugin::default(),
        ))
        .add_systems(Startup, setup)
        .add_systems(Update, check_for_gltf_extras)
        .add_observer(check_insertions)
        .run();
}

fn check_insertions(
    trigger: Trigger<SceneInstanceReady>,
    children: Query<&Children>,
    levels: Query<&PowerLevel>,
) {
    for entity in
        children.iter_descendants(trigger.target())
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
struct PowerLevel {
    energy: f32,
}

#[derive(Component)]
struct ExampleDisplay;

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

    // replace this .gltf file to show data
    commands.spawn(SceneRoot(asset_server.load(
        GltfAssetLabel::Scene(0).from_asset("debug.gltf"),
    )));

    // a place to display the extras on screen
    commands.spawn((
        Text::default(),
        TextFont {
            font_size: 15.,
            ..default()
        },
        Node {
            position_type: PositionType::Absolute,
            top: Val::Px(12.0),
            left: Val::Px(12.0),
            ..default()
        },
        ExampleDisplay,
    ));
}

fn check_for_gltf_extras(
    gltf_extras_per_entity: Query<(
        Entity,
        Option<&Name>,
        Option<&GltfSceneExtras>,
        Option<&GltfExtras>,
        Option<&GltfMeshExtras>,
        Option<&GltfMaterialExtras>,
    )>,
    mut display: Single<&mut Text, With<ExampleDisplay>>,
) {
    let mut gltf_extra_infos_lines: Vec<String> = vec![];

    for (
        id,
        name,
        scene_extras,
        extras,
        mesh_extras,
        material_extras,
    ) in gltf_extras_per_entity.iter()
    {
        if scene_extras.is_some()
            || extras.is_some()
            || mesh_extras.is_some()
            || material_extras.is_some()
        {
            let formatted_extras = format!(
                "Extras per entity {} ('Name: {}'):
    - scene extras:     {:?}
    - primitive extras: {:?}
    - mesh extras:      {:?}
    - material extras:  {:?}
                ",
                id,
                name.unwrap_or(&Name::default()),
                scene_extras,
                extras,
                mesh_extras,
                material_extras
            );
            gltf_extra_infos_lines.push(formatted_extras);
        }
        display.0 = gltf_extra_infos_lines.join("\n");
    }
}
