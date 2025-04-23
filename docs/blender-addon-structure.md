---
title: Blender Addon Structure
description: How the Skein Blender addon works
opengraph_image: /opengraph/opengraph-blender-addon-structure.jpg
---

The Blender addon is a series of Python files in the `extension` directory.

- `__init__.py` is the entrypoint to the entire addon
- `blender_manifest.toml` contains the packaing information for the addon
- Any file that starts with `op_` contains a Blender Operators.
- `skein_panel.py` is the Panel UI for Objects, Meshes, and Materials
- `gltf_export_extension` is the [glTF export extension](https://github.com/KhronosGroup/glTF-Blender-IO) code that handles setting the glTF extras
- `property_groups.py` is the core of the Component's data.
- `form_to_object.py` is basically `PropertyGroup.to_json()` (this "to_json" doesn't exist afaik)
- `object_to_form.py` is the opposite of `form_to_object.py`. It takes JSON data and inserts it into a Component.
- CLI extensions are prefixed with `cli_`

## The Workflow

Workflow-wise, the `FetchRemoteTypeRegistry` operator must be run to fetch the Bevy registry data, which means it must be the first action before being able to insert and modify Component data on objects.

`FetchRemoteTypeRegistry` will store the result of a Bevy Remote Protocol request in a `skein-registry.json` text file. Future opens of the `.blend` file will load the registry data from `skein-registry.json` instead of needing to make a BRP request.

## Processing the Registry

After gaining access to the registry information, we build `PropertyGroup`s dynamically for every single Component type and, because Blender Properties require static typing _and_ don't support rich enums, we build out a large container type that contains a field for every single Component type. The container component type stores information about which Component it is supposed to represent, which is then used to pick the right fields to display in the UI.

Having this large container type allows us to set up a `CollectionProperty` that can support multiple Components.

Inserting Components on Objects, Meshes, or Materials is as easy as inserting one of these container types into the Components `CollectionProperty` on the object, mesh, or material.

## The Skein Panel UI

The SkeinPanel will then introspect the data in the `CollectionProperty`'s `PropertyGroup`s to build forms for the selected Component data.

Using these `PropertyGroup`s is what allows us to take advantage of Blender features like Drivers and Library Overrides.
