---
title: Overview
description: Skein is a Bevy Plugin and a Blender extension that integrates your Bevy App's Component data into Blender's UI
opengraph_image: /opengraph/opengraph-index.jpg
---

[Bevy](https://bevyengine.org/) is a free and open source refreshingly simple data-driven game engine built in Rust.

[Blender](https://www.blender.org/) is free and open source 3D creation software including modelling, animation, and more.

**Skein** is a **Bevy Plugin** and a **Blender extension** that integrates your Bevy App's **Component** data into **Blender's UI**. This enables inserting Bevy Components on Objects, Meshes, and Materials inside of Blender. The inserted Component data is exported alongside .gltf/.glb and instantiated when spawning scenes in Bevy.

## tldr;

1. Register components in Bevy using [`App::register_type`](https://docs.rs/bevy/latest/bevy/prelude/struct.App.html#method.register_type)
1. Insert Bevy Components into objects, meshes, or materials in Blender
1. Export to glTF
1. Components are instantiated when spawning in Bevy

This makes Blender easier to use as a level design tool and game development tool with Bevy.

<!-- ## Use Cases

TODO: link use cases

- Building levels as Blender scenes
- Applying physics colliders to Blender objects
- Marking materials in Blender for replacement using custom shaders in Bevy
- -->
