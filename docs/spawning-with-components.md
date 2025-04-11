---
title: Spawning with Components
description: How to spawn glTF data with components
opengraph_image: /opengraph/opengraph-spawning-with-components.jpg
---

Spawn glTF as usual: https://github.com/bevyengine/bevy/blob/0ab477e2664680c5ff38fbbe4a709284354c154f/examples/3d/load_gltf.rs

```rust
commands.spawn(SceneRoot(asset_server.load(
    GltfAssetLabel::Scene(0).from_asset("models/FlightHelmet/FlightHelmet.gltf"),
)));
```
