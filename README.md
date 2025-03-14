> [!CAUTION]
> in-progress crate.

# Skein

A Bevy Plugin and a Blender extension for improving the efficiency of Bevy/Blender workflows.

tldr:

1. Register components in Bevy
2. Apply Bevy Components to objects, meshes, or materials in Blender
3. Export to glTF
4. Components are instantiated when spawning in Bevy

## Quickstart

Add the plugin and register components (`reflect(Component)` is important!)

```rust
use bevy::prelude::*;
use bevy_skein::SkeinPlugin;

fn main() {
    App::new()
        .register_type::<Player>()
        .add_plugins((
            DefaultPlugins,
            SkeinPlugin::default(),
        ))
        .run();
}

#[derive(Component, Reflect, Debug)]
#[reflect(Component)]
struct Player {
    name: String,
    power: f32,
    test: i32,
}
```

- Install the Blender Addon (todo)
- Fetch the Bevy registry using the Blender Operator
- Select and apply a component
- Export to glTF
- Spawn a Scene from the glTF file, which will have components instantiated

```rust
commands.spawn(SceneRoot(asset_server.load(
    GltfAssetLabel::Scene(0).from_asset("my_export.gltf"),
)));
```

## Use Cases

- Apply Bevy Components in Blender
- Replace materials from Blender with materials defined in Bevy ([example](examples/replace_material.rs))
- Use Blender Drivers to power Bevy Component values

## Why is it named Skein?

Its a tool that aims to improve the efficiency of Bevy (group of birds) and Blender workflows.

> A flock of wild geese or swans in flight, typically in a V-shaped formation.
>
> - [Oxford Dictionary](https://web.archive.org/web/20190107072506/https://en.oxforddictionaries.com/definition/skein)

> A V formation is a symmetric V- or chevron-shaped flight formation. In nature, it occurs among geese, swans, ducks, and other migratory birds, improving their energy efficiency
>
> - [Wikipedia](https://en.wikipedia.org/wiki/V_formation)

Its also thread/yarn related which is cool too.
