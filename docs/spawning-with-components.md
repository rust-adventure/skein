---
title: Spawning with Components
description: How to spawn glTF data with components
opengraph_image: /opengraph/opengraph-spawning-with-components.jpg
---

Spawn glTF as usual, with or without `bsn` by taking advantage of `WorldAssetRoot`.

```rust
commands.spawn(WorldAssetRoot(asset_server.load(
    GltfAssetLabel::Scene(0).from_asset("models/FlightHelmet/FlightHelmet.gltf"),
)));
```

```rust
commands.spawn_scene(bsn!{
    WorldAssetRoot("stuff.gltf#Scene0")
    Transform
});
```
