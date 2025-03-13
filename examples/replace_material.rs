//! How to use `Component` on_add hooks to replace
//! materials defined in Blender.
//!
//! In Blender, a `Component` (`UseDebugMaterial` in this example)
//! can be added to a Material.
//! Any object this Material is attached to will also
//! have this `Component`.
//!
//! This `UseDebugMaterial` has an on_add hook that replaces
//! the `StandardMaterial` with a Bevy handle to another material.
//!
//! In this example we create and store the material handle in a `Resource`
//! at startup, allowing us to re-use the handle as many times as
//! needed. You could use a HashMap instead to handle many handles
//! like this.
//!
use bevy::{
    asset::RenderAssetUsages,
    prelude::*,
    render::render_resource::{
        Extent3d, TextureDimension, TextureFormat,
    },
};
use bevy_ecs::{
    component::ComponentId, world::DeferredWorld,
};
use bevy_skein::SkeinPlugin;

fn main() {
    App::new()
        .register_type::<UseDebugMaterial>()
        .add_plugins((
            DefaultPlugins
                .set(ImagePlugin::default_nearest()),
            SkeinPlugin::default(),
        ))
        .add_systems(Startup, setup)
        .run();
}

fn setup(
    mut commands: Commands,
    mut images: ResMut<Assets<Image>>,
    mut materials: ResMut<Assets<StandardMaterial>>,
    asset_server: Res<AssetServer>,
) {
    // Create and insert a handle to the debug material
    // as a Resource we can access later
    let debug_material = materials.add(StandardMaterial {
        base_color_texture: Some(
            images.add(uv_debug_texture()),
        ),
        ..default()
    });
    commands.insert_resource(DebugMaterial(debug_material));

    // Spawn a camera in to reduce additional gltf data for
    // examples. A camera can also be exported from Blender
    // with the right export settings
    commands.spawn((
        Camera3d::default(),
        Transform::from_xyz(0.0, 7., 14.0)
            .looking_at(Vec3::new(0., 1., 0.), Vec3::Y),
    ));

    commands.spawn(SceneRoot(
        asset_server.load(
            GltfAssetLabel::Scene(0)
                .from_asset("replace_material.gltf"),
        ),
    ));
}

#[derive(Resource)]
struct DebugMaterial(Handle<StandardMaterial>);

#[derive(Component, Reflect)]
#[reflect(Component)]
#[component(on_add = on_add_use_debug_material)]
struct UseDebugMaterial;

/// The on_add hook that will run when the component is
/// added when spawning the glTF scene.
fn on_add_use_debug_material(
    mut world: DeferredWorld,
    entity: Entity,
    _: ComponentId,
) {
    let debug_material =
        world.resource::<DebugMaterial>().0.clone();

    world
        .commands()
        .entity(entity)
        .insert(MeshMaterial3d(debug_material));
}

/// Creates a colorful test pattern
/// taken directly from the examples in the Bevy repo
fn uv_debug_texture() -> Image {
    const TEXTURE_SIZE: usize = 8;

    let mut palette: [u8; 32] = [
        255, 102, 159, 255, 255, 159, 102, 255, 236, 255,
        102, 255, 121, 255, 102, 255, 102, 255, 198, 255,
        102, 198, 255, 255, 121, 102, 255, 255, 236, 102,
        255, 255,
    ];

    let mut texture_data =
        [0; TEXTURE_SIZE * TEXTURE_SIZE * 4];
    for y in 0..TEXTURE_SIZE {
        let offset = TEXTURE_SIZE * y * 4;
        texture_data[offset..(offset + TEXTURE_SIZE * 4)]
            .copy_from_slice(&palette);
        palette.rotate_right(4);
    }

    Image::new_fill(
        Extent3d {
            width: TEXTURE_SIZE as u32,
            height: TEXTURE_SIZE as u32,
            depth_or_array_layers: 1,
        },
        TextureDimension::D2,
        &texture_data,
        TextureFormat::Rgba8UnormSrgb,
        RenderAssetUsages::RENDER_WORLD,
    )
}
