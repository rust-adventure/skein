//! This example is called "without_blender" because
//! it demonstrates all of the Rust-side API without
//! requiring a glTF file, blender usage, or anything
//! else outside of this file.
//!
//! The `Character` component is reflected and registered
//! as usual, which allows the GltfExtras component with
//! the skein data to instantiate a component.
//!
//! This is basically what is happening when you load a .gltf
//! file and spawn a scene but if you're just adding components
//! in your regular Bevy application then you don't need the
//! extra indirection here and should add the components directly
use bevy::{
    color::palettes::tailwind::SKY_400, prelude::*,
};
use skein::SkeinPlugin;

fn main() {
    App::new()
        .register_type::<Character>()
        .add_plugins((
            DefaultPlugins
                .set(ImagePlugin::default_nearest()),
            SkeinPlugin::default(),
        ))
        .add_systems(Startup, setup)
        .run();
}

#[derive(Component, Reflect)]
#[reflect(Component)]
struct Character {
    name: String,
    height: f32,
}

fn setup(
    mut commands: Commands,
    mut materials: ResMut<Assets<StandardMaterial>>,
    mut meshes: ResMut<Assets<Mesh>>,
) {
    commands.spawn((
        Camera3d::default(),
        Transform::from_xyz(0.0, 7., 14.0)
            .looking_at(Vec3::new(0., 1., 0.), Vec3::Y),
    ));

    commands.spawn((
        PointLight {
            shadows_enabled: true,
            intensity: 10_000_000.,
            range: 100.0,
            shadow_depth_bias: 0.2,
            ..default()
        },
        Transform::from_xyz(8.0, 16.0, 8.0),
    ));

    commands.spawn((
        MeshMaterial3d(materials.add(StandardMaterial {
            base_color: SKY_400.into(),
            ..default()
        })),
        Mesh3d(meshes.add(Cuboid::default())),
        Transform::from_xyz(0., 0., 0.),
        GltfExtras {
            value: r#"
{
    "skein": [{
        "without_blender::Character": {
            "name": "Hollow Knight",
            "height": 20.
        }
    }]
}"#
            .to_string(),
        },
    ));
}
