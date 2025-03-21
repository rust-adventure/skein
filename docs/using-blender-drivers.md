---
title: Using Blender Drivers
description: Quidem magni aut exercitationem maxime rerum eos.
---

[Blender Drivers](https://docs.blender.org/manual/en/latest/animation/drivers/index.html) are a way to control values of properties by means of a function, or a mathematical expression.
Drivers can be used to power values in Bevy components, such as using the width, height, and depth of a cube to power an Avian Cuboid Collider's size.
Then when resizing the cube, the collider's values track to the new values.

## Driving Collider fields

We'll be using a Blender Object's `dimensions` in this example. Specifically the default cube's. More data fields can be found [in the docs](https://docs.blender.org/api/current/bpy.types.Object.html#bpy.types.Object.dimensions)

> [!NOTE]
> We start having already inserted a Avian `ColliderConstructor::Cuboid` Component. Read [Inserting Components](/docs/inserting-components) if you need to learn how to do that

### Add a Driver

Right click on a Component value (we're using the `x_length`) and select `Add Driver`

![add driver menu](/images/the-blender-addon/add-driver.avif)

The Driver form will show. Drivers can be as simple as a single property to as complex as arbitrary python.

![add driver form](/images/the-blender-addon/add-driver-form.avif)

We'll select `Single Property`

![add driver single property field](/images/the-blender-addon/add-driver-single-property.avif)

This shows a new form

![single property form](/images/the-blender-addon/single-property-form.avif)

We'll select the default cube as our Object

![add driver select object](/images/the-blender-addon/add-driver-select-object.avif)

Then we'll set the `Path` for our property

![add driver selected cube object](/images/the-blender-addon/add-driver-selected-object.avif)

We'll use `dimensions` to get the x, y, and z length (aka: width, height, and depth).

> [!IMPORTANT]
> Blenders dimensions are Y-up, so dimensions[0] is x, dimensions[1] is y, and dimensions[2] is z.
>
> In Bevy, Z is up, so we need to map Blender's coordinates to the values our components expect in Bevy:
>
> - x -> x_length
> - y -> z_length
> - z -> y_length

![driver path usinge dimensions](/images/the-blender-addon/driver-path-dimensions.avif)

### Repeat for all three values

If you repeat these steps for all three values, all three will be controlled by their respective dimensions.

![three drivers for three values](/images/the-blender-addon/three-drivers.avif)

### Scaling the Cube

Switch into Edit Mode (use `Tab` or the top-left menu)

![switch into edit mode](/images/the-blender-addon/into-edit-mode.avif)

Scale the cube up (hit `s`)

![Scaling the cube in edit mode](/images/the-blender-addon/scaled-cube-in-edit-mode.avif)

Watch as the values grow as the cube scales. This is Drivers.

The values that are driven into the component values will be exported with the glTF export.
