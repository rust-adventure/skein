---
title: Replace a Blender Material
description: Defining Materials in Blender and replacing them with custom Bevy shaders
opengraph_image: /opengraph/opengraph-replace-a-blender-material.jpg
---

Its not uncommon to want to define materials in Blender and replace them with custom shaders in Blender. For example, in Blender you could define a "Force Field" material. This material would import into Bevy as a regular `StandardMaterial` and be applied to any objects it was applied to in Blender.

If you utilize [Hooks and Observers](/docs/mark-and-modify-blender-objects) you can define a marker component that will be inserted alongside this Material, allowing you to replace it with custom shaders utilizing all of Bevy's features.

![bevy application running](/images/use-cases/replace_material.avif)

## A Bevy Material

We'll define a `ForceFieldMaterial` that is based on the [Bevy 0.10 Release Notes Depth and Normals Demo](https://bevyengine.org/news/bevy-0-10/#depth-and-normal-prepass).

View the [shader logic](https://github.com/rust-adventure/skein/blob/2a6a7f8597770b17ed24cabc783e7dd7cf593c9b/assets/shaders/force_field.wgsl) over on GitHub if you want to, but returning a flat color would also work for this example.

```rust
// This is the struct that will be passed to your shader
#[derive(Asset, TypePath, AsBindGroup, Debug, Clone)]
struct ForceFieldMaterial {}

impl Material for ForceFieldMaterial {
    fn fragment_shader() -> ShaderRef {
        "shaders/force_field.wgsl".into()
    }

    fn alpha_mode(&self) -> AlphaMode {
        AlphaMode::Add
    }

    fn specialize(
        _pipeline: &bevy::pbr::MaterialPipeline<Self>,
        descriptor: &mut bevy::render::render_resource::RenderPipelineDescriptor,
        _layout: &bevy::render::mesh::MeshVertexBufferLayoutRef,
        _key: bevy::pbr::MaterialPipelineKey<Self>,
    ) -> Result<(), bevy::render::render_resource::SpecializedMeshPipelineError>{
        descriptor.primitive.cull_mode = None;
        Ok(())
    }
}
```

## Marker Components and Hooks

We'll use a `Component`'s `on_add` hooks to replace materials defined in Blender with our force field when the Bevy application runs.

In Blender, a `Component` (`UseForceField` in this example) can be added to a Material **using the Materials Panel** as detailed in [Inserting Components](/docs/inserting-components).
Any object this Material is attached to will also have this `Component`.

![blender ui](/images/use-cases/replace_material_blend.avif)

This `UseForceFieldMaterial` has an `on_add` hook that replaces the `StandardMaterial` with a Bevy handle to another material.

```rust
#[derive(Component, Reflect)]
#[reflect(Component)]
#[component(on_add = on_add_use_force_field_material)]
struct UseForceFieldMaterial;

/// The on_add hook that will run when the component is
/// added when spawning the glTF scene.
fn on_add_use_force_field_material(
    mut world: DeferredWorld,
    HookContext { entity, .. }: HookContext,
) {
    let force_field = world
        .resource::<MaterialStore>()
        .force_field
        .clone();

    world
        .commands()
        .entity(entity)
        .remove::<MeshMaterial3d<StandardMaterial>>()
        .insert(MeshMaterial3d(force_field));
}
```

## Storing Material Handles

> [!TIP]  
> In this example we create and store the material handle in a `Resource` at startup, allowing us to re-use the handle as many times as needed. You could use a HashMap instead to handle many handles like this or ignore it completely and recreate the material if you don't care.

```rust
#[derive(Resource)]
struct MaterialStore {
    force_field: Handle<ForceFieldMaterial>,
}

fn setup(
    mut commands: Commands,
    mut materials_force_field: ResMut<
        Assets<ForceFieldMaterial>,
    >,
) {
    // Create and insert a handle to the debug material
    // as a Resource we can access later
    commands.insert_resource(MaterialStore {
        force_field: materials_force_field.add(ForceFieldMaterial {}),
    });
}
```

## Trobuleshooting: UVs

> [!CAUTION]  
> Any mesh that hasn't been UV unwrapped may seem like it isn't working. This shows up in .gltf files as a missing `TEXCOORD_0` field. `Suzanne` in the following example glTF data has it, and `rock` does not. This is something you can check for in Blender.

```rust
{
    "name":"Suzanne",
    "primitives":[
        {
            "attributes":{
                "POSITION":28,
                "NORMAL":29,
                "TEXCOORD_0":30
            },
            "indices":31,
            "material":0
        }
    ]
},
{
    "name":"rock",
    "primitives":[
        {
            "attributes":{
                "POSITION":32,
                "NORMAL":33
            },
            "indices":34,
            "material":0
        }
    ]
},
```
