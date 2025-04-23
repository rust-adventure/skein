---
title: Migration Tools
description: Component data can change in various ways over time. Here are some tools to aid that process.
opengraph_image: /opengraph/opengraph-migration-tools.jpg
---

> [!IMPORTANT]
>
> Migration tools are experimental. Make a backup of your .blend file before using any of the tools mentioned in this documentation.

Component data can change over time. Some examples of this include:

- Crate renames, or other module-path changes. [example](https://github.com/bevyengine/bevy/pull/18813)
- The addition, removal, or other modification of fields in a Component

Skein is building some migration tooling to support these cases.

## CLI Tools

Skein's CLI tools are "built in" to Blender when using the addon.

### dump_component_data

Pick a .blend file and find all usages of all components. Write out an object with all usages of all components.

```
blender --background -b replace_material.blend -c dump_component_data -o test.json
```

#### Output

```json
{
  "object": [
    {
      "name": "Camera",
      "components": [
        {
          "type_path": "bevy_core_pipeline::prepass::DepthPrepass",
          "data": {}
        },
        {
          "type_path": "bevy_core_pipeline::prepass::NormalPrepass",
          "data": {}
        },
        {
          "type_path": "bevy_core_pipeline::bloom::settings::Bloom",
          "data": {
            "composite_mode": "EnergyConserving",
            "high_pass_frequency": 1.0,
            "intensity": 0.15000000596046448,
            "low_frequency_boost": 0.699999988079071,
            "low_frequency_boost_curvature": 0.949999988079071,
            "max_mip_dimension": 512,
            "prefilter": {
              "threshold": 0.0,
              "threshold_softness": 0.0
            },
            "scale": [1.0, 1.0]
          }
        }
      ]
    }
  ],
  "mesh": [],
  "material": [
    {
      "name": "Debug",
      "components": [
        {
          "type_path": "replace_material::UseDebugMaterial",
          "data": {}
        }
      ]
    },
    {
      "name": "ForceField",
      "components": [
        {
          "type_path": "replace_material::UseForceFieldMaterial",
          "data": {}
        },
        {
          "type_path": "bevy_pbr::light::NotShadowCaster",
          "data": {}
        },
        {
          "type_path": "bevy_pbr::light::NotShadowReceiver",
          "data": {}
        }
      ]
    }
  ],
  "camera": [],
  "light": [],
  "collection": []
}
```

#### Filtering

Optionally filter the results to match one or more components, which will reduce the output to only include those components.

```
blender --background -b replace_material.blend -c dump_component_data -o test.json -p "replace_material::UseDebugMaterial"
```

```json
{
  "object": [],
  "mesh": [],
  "material": [
    {
      "name": "Debug",
      "components": [
        {
          "type_path": "replace_material::UseDebugMaterial",
          "data": {}
        }
      ]
    }
  ],
  "camera": [],
  "light": [],
  "collection": []
}
```
