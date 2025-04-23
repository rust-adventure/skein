---
title: Component Presets (Default and variants)
description: Using and providing presets for Component values
opengraph_image: /opengraph/opengraph-migration-tools.jpg
---

Components can have `Default` implementations. For example a `PointLight` could have a `Default` implementation as such:

```rust
PointLight {
    color: Color::WHITE,
    intensity: 1_000_000.0,
    range: 20.0,
    radius: 0.0,
    shadows_enabled: false,
    affects_lightmapped_mesh_diffuse: true,
    shadow_depth_bias: 0.08,
    shadow_normal_bias: 0.6,
    shadow_map_near_z: 0.1,
}
```

But `Default` is not the only way to gain pre-set values. Any instantiated value could be treated as a "preset".

## Enabling Presets

Enabling the `presets` feature in the Skein Rust crate will enable a custom BRP endpoint which will serve up possible presets to Blender. Some of these will be the `Default` implementations for Components that offer them. Others can be user-provided via `insert_skein_preset`:

```rust
App::new()
    .insert_skein_preset("Red", PointLight {
        color: Color::RED,
        intensity: 1_000_000.0,
        range: 20.0,
        radius: 0.0,
        shadows_enabled: false,
        affects_lightmapped_mesh_diffuse: true,
        shadow_depth_bias: 0.08,
        shadow_normal_bias: 0.6,
        shadow_map_near_z: 0.1,
    })
```

## Fetching Presets

When you fetch the Bevy registry via the `FetchRemoteTypeRegistry` operator, this will also call the BRP endpoint and store the preset values in a text block called `skein-presets.json` in the .blend file.

## Using Presets

Presets in Blender will show up for the component types. The `default` preset is the Rust `Default` implementation, and this preset is used when inserting a component to set up the initial values.

![defaults and presets](/images/the-blender-addon/defaults-and-presets.avif)
