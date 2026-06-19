use bevy::{
    prelude::*, world_serialization::WorldInstanceReady,
};
use bevy_skein::SkeinPlugin;

fn main() {
    App::new()
        .add_plugins((
            DefaultPlugins,
            SkeinPlugin::default(),
        ))
        .add_observer(
            // log the component from the gltf spawn
            |ready: On<WorldInstanceReady>,
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
        .add_systems(Startup, startup.spawn())
        .run();
}

#[derive(Component, Default, Reflect, Debug)]
#[reflect(Component, Default)]
#[type_path = "api"]
struct Character {
    name: String,
}

fn startup() -> impl Scene {
    bsn! {
        WorldAssetRoot("demo.gltf#Scene0")
    }
}
