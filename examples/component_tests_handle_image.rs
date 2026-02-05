//! An example that is only used to confirm that
//! extension-based skein data is working
//!
//! it renders a cube, and contains a camera and a
//! point light with extension data on basically
//! every object.
use bevy::{math::Affine2, prelude::*};
use bevy_scene::SceneInstanceReady;
use bevy_skein::{SkeinAppExt, SkeinPlugin};
use test_components::*;

#[derive(Debug, Component, Reflect)]
#[reflect(Component)]
#[type_path = "api"]
struct TestImage(Handle<Image>);

fn main() {
    App::new()
        // add plugins
        .add_plugins((
            DefaultPlugins,
            SkeinPlugin::default(),
        ))
        .add_systems(Startup, setup)
        .add_observer(
            |ready: On<SceneInstanceReady>,
             children: Query<&Children>,
             query: Query<&TestImage>,
             mut materials: ResMut<
                Assets<StandardMaterial>,
            >,
             mut commands: Commands| {
                for child in
                    children.iter_descendants(ready.entity)
                {
                    if let Ok(image) = query.get(child) {
                        commands.entity(child).insert(
                            MeshMaterial3d(materials.add(
                                StandardMaterial {
                                    base_color_texture:
                                        Some(
                                            image.0.clone(),
                                        ),
                                    uv_transform:
                                        Affine2::from_scale(
                                            Vec2::splat(
                                                20.,
                                            ),
                                        ),
                                    ..default()
                                },
                            )),
                        );
                    }
                }
            },
        )
        .run();
}

fn setup(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
) {
    commands.spawn(SceneRoot(
        asset_server
            .load(GltfAssetLabel::Scene(0).from_asset(
                "images/scene-with-image.gltf",
            )),
    ));
}
