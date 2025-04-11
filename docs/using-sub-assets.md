---
title: Using Sub-Assets
description: There are many elements of a glTF file, Scenes, Nodes, Meshes, Materials, etc. They can be used piecemeal if you know what you're doing.
opengraph_image: /opengraph/opengraph-using-sub-assets.jpg
---

There are many elements of a glTF file including Scenes, Nodes, Meshes, Materials, Skins, Nodes, AnimationClips, etc. With appropriate care, these elements can be used to build up specific hierarchies for niche use cases.

## Bevy's Gltf struct

Bevy's [`Gltf`](https://docs.rs/bevy/latest/bevy/gltf/struct.Gltf.html) struct contains the processed glTF data, with and without names.

We'll be using named access because its clearer for written instructional content, which means we can use these fields on `Gltf`:

```rust
named_scenes: HashMap<Box<str>, Handle<Scene>>
named_meshes: HashMap<Box<str>, Handle<GltfMesh>>
named_materials: HashMap<Box<str>, Handle<StandardMaterial>>
named_nodes: HashMap<Box<str>, Handle<GltfNode>>
named_skins: HashMap<Box<str>, Handle<GltfSkin>>
named_animations: HashMap<Box<str>, Handle<AnimationClip>>
```

## Spawning a Mesh (Custom Material)

Spawning a mesh from a glTF by itself seems straightforward at first, but Bevy's `Mesh` and `GltfMesh` are not the same concept. A Bevy [`Mesh`](https://docs.rs/bevy/latest/bevy/prelude/struct.Mesh.html) is closer to a [`GltfPrimitive`](https://docs.rs/bevy/latest/bevy/gltf/struct.GltfPrimitive.html) than a [`GltfMesh`](https://docs.rs/bevy/latest/bevy/gltf/struct.GltfMesh.html).

```rust
let handle = gltf.named_meshes.get("Sphere").unwrap();
let gltf_mesh = gltf_meshes.get(handle).unwrap();

commands.spawn((
    Mesh3d(gltf_mesh.primitives[0].mesh.clone()),
    MeshMaterial3d(materials.force_field.clone()),
    gltf_mesh.primitives[0]
        .extras
        .clone()
        .unwrap_or(GltfExtras::default()),
));
```

## Using a Material

You can use materials in two ways: **with** or **without** the Bevy Components you applied in Blender.

### Without Components

To apply a material from a glTF file you can access the handle via `named_meshes` by material name and use the handle directly. This approach is simpler but _will not_ apply the **Components** you inserted in Blender.

```rust
let gltf = gltf.get(&gltf_handle).ok_or("couldn't get gltf")?;
let material_handle = gltf
    .named_materials
    .get("Wooden Panel")
    .ok_or("Couldn't get material handle")?;

commands.spawn((
    Mesh3d(meshes.add(Plane3d::new(
        Vec3::Y,
        Vec2::new(1.5, 1.5),
    ))),
    MeshMaterial3d(material_handle.clone()),
    Transform::from_xyz(0., 0., 0.)
));
```

### With Components

If there are **Components** you applied in Blender that you want to also apply, you must gain access to the `GltfExtras` component and insert it alongside the material handle. If you followed the instructions in [Exporting Materials to Files](/docs/exporting-materials-to-files) then you will have a simple mesh like a Sphere or Cube, which will have a single primitive associated with the material.

Everything here is set up to exist, but we'll use `ok_or()?` anyway because Bevy supports returning `Result` from systems.

```rust
let gltf = gltf.get(&gltf_handle).ok_or("couldn't get gltf")?;
let primitive = &gltf_meshes
    .get(
        gltf.named_meshes
            .get("WallBricksMesh")
            .ok_or("couldn't get gltf_mesh")?,
    )
    .ok_or("couldn't get gltf_primitive")?
    .primitives[0];

commands.spawn((
    Mesh3d(meshes.add(Plane3d::new(
        Vec3::Y,
        Vec2::new(1.5, 1.5),
    ))),
    MeshMaterial3d(
        primitive
            .material
            .clone()
            .ok_or("Option was None")?,
    ),
    Transform::from_xyz(0., 0., 0.),
    primitive
        .material_extras
        .clone()
        .ok_or("Option was None")?,
));
```
