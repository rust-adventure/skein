---
title: Property Groups
description: How Skein uses PropertyGroups to create Component forms and other data
opengraph_image: /opengraph/property-groups.jpg
---

Blender has two concepts for custom data: Properties and IDData

ID data can be arbitrary Python values, but come with restrictions that make building UI from them difficult. Thus we use Properties which come with their own restrictions.

## What are PropertyGroups?

[`PropertyGroups`][property-group] are _the_ way to emulate any kind of dict/struct in Blender's Property class system. This means they are the way we emulate Component values from Bevy.

> [!NOTE]
>
> `PropertyGroups` can not be nested by themselves, you _must_ wrap a `PropertyGroup`-derived class in a [`PointerProperty`][pointer-property] to be editable. Otherwise properties can fail to show up when dealing with the values when programming.

```python
# Example from Blender docs
import bpy

class MyPropertyGroup(bpy.types.PropertyGroup):
    custom_1: bpy.props.FloatProperty(name="My Float")
    custom_2: bpy.props.IntProperty(name="My Int")


bpy.utils.register_class(MyPropertyGroup)

bpy.types.Object.my_prop_grp = bpy.props.PointerProperty(type=MyPropertyGroup)

# test this worked
bpy.data.objects[0].my_prop_grp.custom_1 = 22.0
```

## Properties on Objects

Properties can be attached to a number of different objects as "static" types, including the `WindowManager`, `Scene`, `Object`, `Mesh`, or `Material`. This results in _every_ element of that type having an initialized value of the corresponding type.

Here's an example of setting a `selected_component` field on the _type_ of `WindowManager`. Roughly speaking: `bpy.types` is the type, and `bpy.props` are values. This is critically important when setting new fields on types.

```python
bpy.types.WindowManager.selected_component = bpy.props.StringProperty(
    name="component type path",
    description="The component that will be added if selected",
    update=on_select_new_component,
)
```

## Library Overrides

Components can be set on Blender Objects in Blender Collections that are used as Blender Assets. These assets can be instanced into another Blender Scene and the Component `PropertyGroup` values (or other data) can be overridden using [**Library Overrides**](https://docs.blender.org/manual/en/latest/files/linked_libraries/library_overrides.html).

It is _critically important_ that _every item in the entire hierarchy of Properties_ includes the [`override={"LIBRARY_OVERRIDABLE"}`](https://docs.blender.org/api/current/bpy_types_enum_items/property_override_flag_collection_items.html#rna-enum-property-override-flag-collection-items) field. If this detail is not maintained across the entire hierarchy, then values overridden on Component `PropertyGroup` fields for instanced assets can behave erratically, such as being capable of being modified but not actually saved into a .blend file.

> [!CAUTION]
>
> You will not get any notification that there is an error if this `override` invariant is not maintained. The values will simply behave erratically.

> [!NOTE]
> A new ["Dynamic Overrides"](https://code.blender.org/2024/12/the-future-of-overrides/) feature may make simple overrides easier in the future.
>
> > Overrides will be one of the main targets for 2025.

[property-group]: https://docs.blender.org/api/current/bpy.types.PropertyGroup.html
[pointer-property]: https://docs.blender.org/api/current/bpy.types.PointerProperty.html
