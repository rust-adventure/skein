---
title: Exporting Materials to Files
description: You can use Blender as a way to visually prepare StandardMaterials.
opengraph_image: /opengraph/opengraph-exporting-material-libraries.jpg
---

Blender is useful for creating a library of Materials inside of Blender. For the most part these materials will be used in the levels and scenes in Blender and exported with their usage when exporting to glTF, which requires no additional steps.

However, you _can_ access materials as sub-assets from glTF files and apply them dynamically to procedural objects in Bevy.

## Exporting Materials

Materials must be applied to some object to be included in a glTF export. If you want to create a material library two options are:

- Export a single glTF with all materials applied to objects
- Use [Collection Exporters](/docs/exporting-multiple-collections)

Both approaches require the same steps.

1. Add a simple mesh such as a **Cube** or a **UV Sphere** to the **Scene**
2. Export the entire glTF or trigger your configured **Collection Exporters**

The only difference is the number of glTF files you have at the end.

The "entire glTF" approach will contain all materials while the **Collection Exporter** approach will result in a glTF file for each object.

Each material can then be used as detailed in [Using Sub-Assets](/docs/using-sub-assets).

> [!NOTE]
>
> Remember! Using sub-assets requires manually managing the `GltfExtras` if you've added Components you want to use along with the materials you're exporting. How to do this is detailed in [Using Sub-Assets](/docs/using-sub-assets).

## Demo

The following image showcases a set of materials applied to spheres and exported. The same materials are then used as sub-assets and applied to `Plane`s programmatically using the `Handle<StandardMaterial>` from the `Gltf` asset.

![material library](/images/advanced-use-cases/material-library-bevy.avif)

The .blend file looks like this

![material library in Blender](/images/advanced-use-cases/material-library-blender.avif)
