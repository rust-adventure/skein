use bevy::{prelude::*, scene::SceneInstanceReady};
use bevy_skein::SkeinPlugin;

fn main() {
    App::new()
        .register_type::<Character>()
        .add_plugins((
            DefaultPlugins,
            SkeinPlugin::default(),
        ))
        .add_observer(
            // log the component from the gltf spawn
            |ready: On<SceneInstanceReady>,
             children: Query<&Children>,
             characters: Query<&Character>| {
                for entity in
                    children.iter_descendants(ready.entity)
                {
                    let Ok(character) =
                        characters.get(entity)
                    else {
                        continue;
                    };
                    info!(?character);
                }
            },
        )
        .add_systems(Startup, startup)
        .run();
}

#[derive(Component, Reflect, Debug)]
#[reflect(Component)]
struct Character {
    name: String,
}

fn startup(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
) {
    commands.spawn(SceneRoot(asset_server.load(
        // Change this to your exported gltf file
        GltfAssetLabel::Scene(0).from_asset("demo.gltf"),
    )));
}
