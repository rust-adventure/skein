---
title: Collection Instances and Library Overrides
description: Blender includes the ability to instance Collections and link assets from other .blend files
opengraph_image: /opengraph/opengraph-collection-instances-and-library-overrides.jpg
---

Blender has a number of ways to link data around, including: **Collection Instances** and **Library Overrides**.

> ![WARNING] > `Object` data and `Object Data` are [_NOT THE SAME THING_](https://docs.blender.org/manual/en/latest/scene_layout/object/introduction.html)

## Collection Instances

[**Collection Instances**](https://docs.blender.org/manual/en/latest/scene_layout/object/properties/instancing/collection.html) allow you to create an instance of a collection for each instance of another object. This can be useful for duplicating the same object tree around without changing anything about it. This includes Component data.

Collection instances can be [made "real"](https://docs.blender.org/manual/en/latest/scene_layout/object/editing/apply.html#bpy-ops-object-duplicates-make-real) which turns them into their own standalone objects which can then be edited independently, including Component data.

TODO: Screenshots of collection instances

## Library Overrides

[**Library Overrides**](https://docs.blender.org/manual/en/latest/files/linked_libraries/library_overrides.html) is a system designed to allow editing linked data, while keeping it in sync with the original library data. Most types of linked data-blocks can be overridden, and the properties of these overrides can then be edited. When the library data changes, unmodified properties of the overridden one will be updated accordingly.

Once you create an Asset in a separate .blend file, and instantiate a linked instance from that asset, **Library Overrides** allow you to override data represented by those linked assets, including Component data.

TODO: screenshots and workflow for library overrides

## Duplicated Objects

### Linked

### Not Linked

- Collection Instance:
  - Linked Everything
  - Not Transform, etc
- Duplicated Object (linked)
  - (alt-D)
  - linked data is MESH DATA, NOT OBJECT PANEL
- Duplicated Object (not-linked)
  - shift-D
  - All Data is copied
- Linked Override
  - Collection Instance from other .blend file
  - Has special support for overriding data using "Library Overrides"
