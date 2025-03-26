---
title: "Exporting: Multiple Collections"
description: Collection Exporters can be used to export as many Blender Collections to separate .gltf files as you want
opengraph_image: /opengraph/opengraph-exporting-multiple-collections.jpg
---

At this point you've likely already exported your entire project as a single .gltf/.glb file. This type of export is great for game jams, prototypes, and more but as a project gets bigger sometimes you'll want to export a bunch of different collections to different .gltf/.glb files, such as a whole bunch of different levels or individual assets you want to programmatically place in the world.

## Collection Exporters

For this Blender has introduced [Collection Exporters](https://docs.blender.org/manual/en/latest/scene_layout/collections/collections.html#exporters). Each collection in your .blend file can be exported to a number of various file formats, although Skein only handles glTF.

### Exporting a Collection

Lets say we have a set of Collections that we'd like to place in the world ourselves, programatically, at arbitrary times in our application's lifecycle. Maybe we're using them for procedual generation. Here's a **Gate** and a **TreasureChest**.

![two collections](/images/the-blender-addon/two-collections.avif)

If we select a Collection, such as the **Gate** and navigate to the white Collection box icon's tab, we can scroll down and see the `Exporters` panel.

![collection panel](/images/the-blender-addon/collection-exporters.avif)

Clicking the `+` icon allows the selection of `glTF 2.0`, which is the same mode we used in [Exporting: The Basics](/docs/exporting-the-basics).

![Select gltf](/images/the-blender-addon/collection-exporter-gltf.avif)

### Configuring an Exporter

The `glTF 2.0` export options show below the `Exporters` list.

> [!TIP]
>
> Blender has special syntax for "file paths next to the .blend file". You can see this in the default export filepath: `//Gate.glb` where `//` is the directory of the current .blend file.

![gltf export options](/images/the-blender-addon/collection-exporter-gltf-options.avif)

### Triggering Exports

While any individual **Collection Exporter** can be triggered by clicking the export buttons in the `Exporters` panel, we can also trigger an export of _all_ configured collection exporters at the same time using the `File` menu

![export all collections](/images/the-blender-addon/export-all-collections.avif)

> [!TIP]
>
> glTF files are self-contained and do not contain references to other glTF assets. You can not create a "dependency graph" of glTF files with cross-referenced assets.
>
> Consider each glTF file as a standalone package of assets
