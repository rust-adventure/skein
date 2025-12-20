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
      "name": "ActivationSensor",
      "components": [
        {
          "avian3d::collision::collider::constructor::ColliderConstructor": {
            "Sphere": {
              "radius": 0.4999999403953552
            }
          }
        }
      ],
      "unrecognized_components": ["tunic_bush::BushSensor"]
    },
    {
      "name": "Blade",
      "components": [],
      "unrecognized_components": ["tunic_bush::Bush"]
    }
  ],
  "mesh": [],
  "material": [
    {
      "name": "TerrainMat",
      "components": [
        {
          "api::TerrainMat": {}
        }
      ]
    }
  ],
  "scene": [],
  "camera": [],
  "light": [],
  "collection": [],
  "bone": []
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

## change_component_path

Replace an old Component path with a new Component path.

> [!WARNING]
> Back up your blend file before using this command. It will mutate data and save the file

```
blender --background -b art/tunic.blend -c change_component_path --old_path tunic_bush::BushSensor --new_path api::BushSensor
```

The output shows the names of components that were modified

```json
{
  "object": ["ActivationSensor"],
  "mesh": [],
  "material": [],
  "scene": [],
  "collection": []
}
```
