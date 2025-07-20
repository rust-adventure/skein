# Skein

A Bevy Plugin and a Blender extension for improving the efficiency of Bevy/Blender workflows: Store reflected component data in glTF extras using software like Blender, and insert components based on those extras.

tldr:

1. Register components in Bevy
2. Apply Bevy Components to objects, meshes, or materials in Blender
3. Export to glTF
4. Components are instantiated when spawning in Bevy

## Quickstart

Add the plugin and register components (`reflect(Component)` is important!)

```rust no_run
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

- Install the Blender Addon\Extension
  * drag and drop the [zip](https://github.com/rust-adventure/skein/releases) file onto Blender's viewport
  * click `install from disk`
- Fetch the Bevy registry using the Blender Operator
- Select and apply a component
- Export to glTF
- Spawn a Scene from the glTF file, which will have components instantiated

```rust ignore
commands.spawn(SceneRoot(asset_server.load(
    GltfAssetLabel::Scene(0).from_asset("my_export.gltf"),
)));
```

## Use Cases

- Apply Bevy Components in Blender
- Replace materials from Blender with materials defined in Bevy ([example](examples/replace_material.rs))
- Use Blender Drivers to power Bevy Component values

## Compatible Bevy versions

The Bevy plugin and the Blender addon have separate release cycles and versions. The contact points are the BRP Registry API format for ingesting Bevy data into Blender and the glTF format we store data in to get data back into Bevy. These clearly-defined API points mean the Bevy Plugin and the Blender addon can evolve independently.

All versions of `bevy_skein` are currently compatible with all versions of the `skein` Blender addon.

| Bevy version | `bevy_skein` version |
| :----------- | :------------------- |
| `0.16`       | `main`               |
| `0.16`       | `0.2`                |
| `0.15`       | `0.1`                |

| Blender version | `skein` addon version |
| :-------------- | :-------------------- |
| `>4.2`          | `0.1+`                |
| `>4.2`          | branch `main`         |

## Why is it named Skein?

Its a tool that aims to improve the efficiency of Bevy (group of birds) and Blender workflows.

> A flock of wild geese or swans in flight, typically in a V-shaped formation.
>
> - [Oxford Dictionary](https://web.archive.org/web/20190107072506/https://en.oxforddictionaries.com/definition/skein)

> A V formation is a symmetric V- or chevron-shaped flight formation. In nature, it occurs among geese, swans, ducks, and other migratory birds, improving their energy efficiency
>
> - [Wikipedia](https://en.wikipedia.org/wiki/V_formation)

Its also thread/yarn related which is cool too.
