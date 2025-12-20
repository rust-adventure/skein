//! An example that is only used to confirm that
//! extension-based skein data is working
//!
//! it renders a cube, and contains a camera and a
//! point light with extension data on basically
//! every object.
use bevy::prelude::*;
use bevy_scene::SceneInstanceReady;
use bevy_skein::{SkeinAppExt, SkeinPlugin};
use test_components::*;

fn main() {
    App::new()
        .insert_skein_preset(
            "Luigi",
            TeamMember {
                player: Player {
                    name: "Luigi Mario".to_string(),
                    power: 100.,
                    test: 5,
                },
                team: Team::Green,
            },
        )
        // add plugins
        .add_plugins((
            DefaultPlugins,
            SkeinPlugin::default(),
        ))
        .add_systems(Startup, setup)
        .add_observer(
            |ready: On<SceneInstanceReady>,
             children: Query<&Children>,
             query: Query<(
                Option<&TeamMember>,
                Option<&Player>,
                Option<&PointLight>,
                Option<&Mesh3d>,
                Option<&Camera>,
                Option<&Children>,
            )>| {
                for child in
                    children.iter_descendants(ready.entity)
                {
                    println!(
                        "{:?}\n    {:?}",
                        child,
                        query.get(child)
                    );
                }
            },
        )
        .run();
}

fn setup(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
) {
    commands.spawn(SceneRoot(asset_server.load(
        GltfAssetLabel::Scene(0).from_asset(
            "test_extension_data/bevy_skein_extension_usage.gltf",
        ),
    )));
}
