---
title: Contributing
description: How the project is structured and internals
opengraph_image: /opengraph/opengraph-overview_1.jpg
---

Skein is a two-piece project:

- A Rust crate
- The Blender extension

## Rust Crate

The Rust crate is fairly small compared to the Python extension.
It relies on Bevy's Reflection infrastructure and consists of

- BRP configuration
- a BRP endpoint to fetch preset/default values for Components
- An Observer that takes glTF extras and inserts the reflected component values

## Blender Extension

The Blender extension is written in Python and its architecture is heavily dependent on how Blender does things.

In general, Blender will not show UI for anything that isn't a Property, so all Component data is converted into PropertyGroups.

The whole Blender extension is dedicated to storing data in these PropertyGroups that represent Component data, and then formatting it into glTF extras using an export extension.
