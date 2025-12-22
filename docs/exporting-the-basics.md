---
title: "Exporting: The Basics"
description: The basics of exporting glTF with Skein
opengraph_image: /opengraph/opengraph-exporting-the-basics.jpg
---

The Blender addon includes Bevy Component data when exporting to glTF.
There are two forms of glTF data Blender can export. `.glb` and `.gltf`.

- `.glb` is the binary form of the data, its the same data as the `.gltf` but wrapped up for production use cases.
- `.gltf` is a JSON file with a sidecar binary blob that contains vertex and other data.

Assuming we've set up Scenes in Blender, we'll export a single glTF file.

## Exporting glTF

In the file menu choose `gltf` from the `Export` menu

![Export glTF](/images/the-blender-addon/export-menu.avif)

If you want to look at the output, then pick `.gltf`. For production you'll want `.glb`.

![glTF or glb](/images/the-blender-addon/glb-or-gltf.avif)

### The exported data

Skein supports two export modes currently.
The Extension data is the modern form, and the Extras data is the older form.
Utilizing Extension data in Bevy was not possible until 0.18, so the older Extras form is still supported but you should prefer the Extension approach.

Assuming we inserted a Component named `Character` structured like this

```rust
#[derive(Component, Reflect)]
#[reflect(Component, Default)]
#[type_path = "api"]
struct Character {
    name: String
}
```

Then the exported `.gltf` file with one Component that was applied to a Blender Empty Object would look like this:

```json
{
  "asset": {
    "generator": "Khronos glTF Blender I/O v4.2.57",
    "version": "2.0"
  },
  "scene": 0,
  "scenes": [
    {
      "name": "Scene",
      "nodes": [0]
    }
  ],
  "nodes": [
    {
      "extensions": {
        "BEVY_skein": {
          "components": [
            {
              "api::Character": {
                "name": "Hollow Knight"
              }
            }
          ]
        }
      },
      "name": "Empty"
    }
  ]
}
```

The older, extras-style output looks like this.

```json
{
  "asset": {
    "generator": "Khronos glTF Blender I/O v4.2.57",
    "version": "2.0"
  },
  "scene": 0,
  "scenes": [
    {
      "name": "Scene",
      "nodes": [0]
    }
  ],
  "nodes": [
    {
      "extras": {
        "skein": [
          {
            "api::Character": {
              "name": "Hollow Knight"
            }
          }
        ]
      },
      "name": "Empty"
    }
  ]
}
```
