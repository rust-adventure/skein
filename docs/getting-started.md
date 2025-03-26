---
title: Getting Started
description: Your first steps with Skein, Bevy, and Blender
opengraph_image: /opengraph/opengraph-getting-started.jpg
---

To make use of Skein, you'll want to [install](/docs/installation) the Bevy Plugin and the Blender addon.

Any Components that are registered with the [`TypeRegistry`](https://docs.rs/bevy/latest/bevy/reflect/struct.TypeRegistry.html) in your Bevy App are made available to the Blender addon over the [Bevy Remote Protocol](https://docs.rs/bevy/latest/bevy/remote/index.html)'s HTTP endpoints.

This information is then stored in your .blend file (the Bevy App only needs to be running if you're updating the registry information) and used to power Component selection and insertion inside of Blender on the Object, Mesh, and Material Properties pages.

To export, Skein applies itself when exporting glTF from Blender. The data of the components you've inserted lives in the exported glTF files and is inserted when spawning scenes in Bevy.
