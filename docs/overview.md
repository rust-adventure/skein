---
title: Overview
description: Skein is a Bevy Plugin and a Blender extension that integrates your Bevy App's Component data into Blender's UI
opengraph_image: /opengraph/opengraph-index.jpg
---

[Bevy](https://bevyengine.org/) is a free and open source refreshingly simple data-driven game engine built in Rust.

[Blender](https://www.blender.org/) is free and open source 3D creation software including modelling, animation, and more.

**Skein** is a **Bevy Plugin** and a **Blender extension** that integrates your Bevy App's **Component** data into **Blender's UI**. This enables inserting Bevy Components on Objects, Meshes, Materials, and more inside of Blender. The inserted Component data is exported inside of your .gltf/.glb and instantiated when spawning scenes in Bevy.

## tldr;

1. Register **Components** in Bevy using [`App::register_type`](https://docs.rs/bevy/latest/bevy/prelude/struct.App.html#method.register_type)
   - In Bevy 0.17 this registration is automatic
1. Fetch the registry information from your Bevy app and store it in Blender
1. Insert Bevy Components into objects, meshes, materials, and more in Blender
1. Export to one big glTF or many small glTF files
1. Components are instantiated when spawning scenes in Bevy

This makes Blender easier to use as a level design and game development tool with Bevy.

<!-- ## Use Cases

TODO: link use cases

- Building levels as Blender scenes
- Applying physics colliders to Blender objects
- Marking materials in Blender for replacement using custom shaders in Bevy
- -->
