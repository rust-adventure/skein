---
title: Collection Instances and Library Overrides
description: Blender includes the ability to instance Collections and link assets from other .blend files
opengraph_image: /opengraph/opengraph-collection-instances-and-library-overrides.jpg
---

Blender has a number of ways to link data around, including: **Collection Instances**, **Duplicated Objects**, and **Library Overrides**.

## Collection Instances

[**Collection Instances**](https://docs.blender.org/manual/en/latest/scene_layout/object/properties/instancing/collection.html) allow you to create an instance of a collection for each instance of another object. This can be useful for duplicating the same object tree around without changing anything about it. This includes Component data.

Given a second Scene named `Miscellaneous`, we can create a `TreasureChest` with a hierarchy of meshes and objects. This mirrors the more complicated real-world situation we might find ourselves in rather than a basic Cube. Each object in the hierarchy has its own Components, such as a Collider for the lid and a separate one for the base.

![chest components](/images/the-blender-addon/chest-components.avif)

![chest lid components](/images/the-blender-addon/chest-lid-components.avif)

We can create a Collection Instance or two of the `TreasureChest`.

![TreasureChest instance](/images/the-blender-addon/create-treasure-chest-instance.avif)

Notice how we don't get any access to the hierarchy we saw earlier. Both Collection instances add an extra node in the hierarchy that contains the instance but we can't access any of the Component data we defined on any items in the hierarchy.

![instanced chests](/images/the-blender-addon/multiple-instanced-chests.avif)

Collection Instances are great for "exact instances" that you want to place in different areas in a level, but not very good for overriding any component values. New Components can be added to the node that is a parent of the `TreasureChest` hierarchy however.

### Making Collection Instances "Real"

Collection instances can be [made "real"](https://docs.blender.org/manual/en/latest/scene_layout/object/editing/apply.html#bpy-ops-object-duplicates-make-real) which turns them into their own standalone objects which can then be edited independently, including Component data.

Here I'm searching for the **Make Instances Real** operator

![Make Instances Real](/images/the-blender-addon/make-instances-real.avif)

Which then results in a full hierarchy copy of the `TreasureChest`, if you select the `Parent` and `Keep Hierarchy` options. These options aren't necessary but it does produce the result you likely expected.

![Make instances real options](/images/the-blender-addon/make-instances-real-options.avif)

Components on these copies can be freely modified without affecting the original hierarchy.

---

## Duplicated Objects

Duplicated Objects are kind-of like Collection Instances, except instead of being instances we're duplicating some subset of the data.

Notably it is **"Duplicate Objects"** and not **"Duplicate Collections"**. This method only works on the orange objects, not collections.

> [!WARNING]
>
> `Object` data and `Object Data` are [_NOT THE SAME THING_](https://docs.blender.org/manual/en/latest/scene_layout/object/introduction.html) which is a critical point to understand the difference between "linked" and "unlinked" duplicates

### Unlinked

**Unlinked** Duplicated Objects can be created with `Shift+D` or searching for **Duplicate Objects**.

![Unlinked Duplicate Object](/images/the-blender-addon/duplicate-object-unlinked.avif)

In an Unlinked Duplicate Object, all data is copied and it is fully independent.

### Linked

**Linked** Duplicated Objects can be created with `Alt+D` or searching for **Duplicate Objects** and checking the **Linked** checkbox.

![Linked Duplicate Object](/images/the-blender-addon/duplicate-object-linked.avif)

When choosing to link data, the linked data is the green **Mesh data** panel, not the data in the orange Object panel.

- Adding components to the green mesh data tab will share those components amongst all linked duplicates.
- Adding components to the orange object panel will be unique to the object.

> [!TIP]
>
> Note that when exported and spawned in Bevy this data represents two nodes. The orange Object data is on the parent node while the green Mesh data is on the child node.

## Library Overrides

[**Library Overrides**](https://docs.blender.org/manual/en/latest/files/linked_libraries/library_overrides.html) is a system designed to allow editing linked data, while keeping it in sync with the original library data. Most types of linked data-blocks can be overridden, and the properties of these overrides can then be edited. When the library data changes, unmodified properties of the overridden one will be updated accordingly.

Once you create an Asset in a separate .blend file, and instantiate a linked instance from that asset, **Library Overrides** allow you to override data represented by those linked assets, including Component data.

TODO: screenshots and workflow for library overrides

- Linked Override
  - Collection Instance from other .blend file
  - Has special support for overriding data using "Library Overrides"
