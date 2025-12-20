---
title: Getting Started
description: Your first steps with Skein, Bevy, and Blender
opengraph_image: /opengraph/opengraph-getting-started.jpg
---

To make use of **Skein**, you'll want to [install](/docs/installation) the **Bevy Plugin** (`bevy_skein`) and the **Blender addon**.

Any **Components** that are registered with the [`TypeRegistry`](https://docs.rs/bevy/latest/bevy/reflect/struct.TypeRegistry.html) in your Bevy App are made available to the Blender addon over the [Bevy Remote Protocol](https://docs.rs/bevy/latest/bevy/remote/index.html)'s HTTP endpoints. After deriving `Reflect` and reflecting `Component` information:

> [!NOTE]  
> Component registration is done automatically in most circumstances in Bevy 0.17 and later releases.
> If you have generic types or want to register manually for any reason you can use [`App::register_type`](https://docs.rs/bevy/latest/bevy/prelude/struct.App.html#method.register_type) to add the type to the registry and make it available via BRP to Blender.

```rust
#[derive(Component, Reflect, Default)]
#[reflect(Component, Default)]
#[type_path = "api"]
struct MyComponent {
    name: String
}

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .run();
}
```

This information is then stored in your `.blend` file (the Bevy App only needs to be running if you're updating the registry information) and used to power Component selection and insertion inside of Blender on the Object, Mesh, Material, etc properties pages.

Skein applies the information you've inserted when exporting glTF from Blender. The data of the components you've inserted is included the exported glTF files and is inserted when spawning scenes in Bevy.
