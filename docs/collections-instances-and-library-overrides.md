---
title: Collection Instances and Library Overrides
description: Blender includes the ability to instance Collections and link assets from other .blend files
opengraph_image: /opengraph/opengraph-index.jpg
---

Blender has a number of ways to link data around, including: **Collection Instances** and **Library Overrides**.

## Collection Instances

[**Collection Instances**](https://docs.blender.org/manual/en/latest/scene_layout/object/properties/instancing/collection.html) allow you to create an instance of a collection for each instance of another object. This can be useful for duplicating the same object tree around without changing anything about it. This includes Component data.

Collection instances can be [made "real"](https://docs.blender.org/manual/en/latest/scene_layout/object/editing/apply.html#bpy-ops-object-duplicates-make-real) which turns them into their own standalone objects which can then be edited independently, including Component data.

TODO: Screenshots of collection instances

## Library Overrides

[**Library Overrides**](https://docs.blender.org/manual/en/latest/files/linked_libraries/library_overrides.html) is a system designed to allow editing linked data, while keeping it in sync with the original library data. Most types of linked data-blocks can be overridden, and the properties of these overrides can then be edited. When the library data changes, unmodified properties of the overridden one will be updated accordingly.

Once you create an Asset in a separate .blend file, and instantiate a linked instance from that asset, **Library Overrides** allow you to override data represented by those linked assets, including Component data.

TODO: screenshots and workflow for library overrides
