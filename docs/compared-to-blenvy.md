---
title: Compared to Blenvy
description: A comparison to the blenvy crate
opengraph_image: /opengraph/opengraph-compared-to-blenvy.jpg
---

A comparison of Skein and Blenvy.

## Skein Design Goals

For comparison's sake, its worth re-iterating some of Skein's design goals:

Skein's design goals include the maintainability of the project and a deep integration with Bevy and Blender.

As a result, from a maintainability perspective, Skein avoids creating new abstractions when possible and puts extra effort into making it easy to upgrade the Bevy crate from version to version.

As a result, from a deep integration perspective, Skein has no bevy-side API surface besides adding the plugin. Spawning scenes from .gltf files requires the same code as without Skein.

Similarly, in Blender, Skein relies on built-in concepts such as PropertyGroups and the glTF exporter extensions. This results in features like Blender's Drivers, Linked Duplicates, and Library Overrides working with Bevy Component data and [future work](https://code.blender.org/2024/12/the-future-of-overrides/) should also benefit Skein's addon experience.

### Examples

- Skein expects you to use Bevy's built in gltf loading functionality. Tools like bevy_asset_loader work as expected.
- Skein expects the user to understand Blender features like collection exporters if multiple .gltf files or "Blueprints" are desired.

## What is Blenvy

[blenvy](https://github.com/kaosat-dev/Blenvy) is a Blender integration crate with an [alpha Bevy 0.14 release](https://github.com/kaosat-dev/Blenvy/releases/tag/blenvy_v0.1.0_pre_alpha). It was the first widely known Blender/Bevy crate and [influenced](https://github.com/bevyengine/bevy/pull/16882) the initial Bevy Remote Protocol registry endpoint.

Similar to Skein, Blenvy provides Blender UI to insert Components and exports that data in gltf files. Blenvy aims to handle a lot more than this though and includes implementations of:

- A prefab format ([Blueprints](https://github.com/kaosat-dev/Blenvy/tree/03cc100caca642b9386630e203e86500208fecf6/examples/blueprints))
- Custom glTF asset loading
- [Game world Save/load](https://github.com/kaosat-dev/Blenvy/tree/03cc100caca642b9386630e203e86500208fecf6/examples/save_load)
- "Material libraries"
- Animation helper components
- Custom [spawning interface](https://github.com/kaosat-dev/Blenvy/blob/03cc100caca642b9386630e203e86500208fecf6/examples/blueprints/src/main.rs#L45-L60) (via Components)
- Blenvy also includes an "Export on save" feature that runs exports for Blueprints, Levels, Materials, and Animations.

## Technical Notes

A light overview for people familiar with implementation details.

Blenvy's component storage is accomplished via a Python implementation of serialization to a RON string in the `bevy_components` glTF extras field, and the export is executed by creating a set of [temporary scenes](https://github.com/kaosat-dev/Blenvy/blob/03cc100caca642b9386630e203e86500208fecf6/tools/blenvy/add_ons/auto_export/common/generate_temporary_scene_and_export.py).

```json
{
    "extras": {
        "bevy_components": "{\"wash_cycle::customer_npc::CustomerDropoffLocation\": \"()\", \"avian3d::collision::collider::Sensor\": \"()\", \"avian3d::collision::collider::constructor::ColliderConstructor\": \"Cuboid(x_length: 1.0, y_length: 0.0, z_length: 1.0)\"}"
    },
    "mesh": 8,
    "name": "CustomerDropoff",
    "translation": [
        -3.984670639038086,
        0.07567913085222244,
        -3.202132225036621
    ]
},
```

Functionally, Blenvy's export is handled by programmatically creating temporary scenes and also includes additional data in fields like `BlueprintAssets`. Blueprints, Levels, Materials, and Animations each have [their own export logic](https://github.com/kaosat-dev/Blenvy/tree/03cc100caca642b9386630e203e86500208fecf6/tools/blenvy/add_ons/auto_export).

```json
"scenes": [
    {
      "extras": {
        "qbaker": {},
        "uuid": "6b58bfb9-5cf6-4499-a01c-b8fc2624d08d",
        "assets reported": {},
        "BlueprintAssets": "(assets: [(name: \"washing_machine\", path: \"blueprints/washing_machine.glb\"), (name: \"colormap.002\", path: \"materials/colormap.002.glb\"), (name: \"Table\", path: \"blueprints/Table.glb\"), (name: \"Tabletop\", path: \"materials/Tabletop.glb\")])"
      },
      "name": "__temp_scene",
      "nodes": [...]
      ...
    }
    ...
]
```

Exporting to individual Material files is accomplished through the creation of isolated, minimal scenes.

```json
  "scenes": [
    {
      "name": "__materials_scene",
      "nodes": [
        0
      ]
    }
  ],
```
