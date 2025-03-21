---
title: Inserting Components
description: Quidem magni aut exercitationem maxime rerum eos.
---

_After_ fetching the **Bevy Type Registry** information; **Components** can be inserted on Blender **Objects**, **Meshes**, and **Materials**.

After selecting an **Object**, the UI for this exists in the **Properties** area in the **Object** tab. You may need to scroll down to see the **Skein Bevy Panel**.

In the **Skein Bevy Panel**, there's an empty field labelled `type:`.

![Object Panel](/images/the-blender-addon/object-panel.avif)

This field will autocomplete on the full type_path for all applicable Components.

![Inserting Component](/images/the-blender-addon/inserting-component.avif)

Once you choose a Component's type_path, the component must be inserted using the Button below labelled **Insert Bevy Component**.

![Inserted Component](/images/the-blender-addon/inserted-component.avif)

After inserting Components, Selecting any component in the list allows you to edit the relevant values, if there are any.

![Editing Component](/images/the-blender-addon/editing-component.avif)

Unit stucts, such as Marker components, will show a message stating that there isn't any data to modify.

![Marker Components](/images/the-blender-addon/marker-components.avif)

---

## Objects, Meshes, and Materials

Objects, Meshes, and Materials are all located in slightly different places in the Blender UI and all of them can receive components.

### Objects

Components can be inserted on Objects, as we covered earlier in this document under the <span class="text-orange-500 dark:text-orange-400">orange square</span> icon.

![Object Panel](/images/the-blender-addon/object-panel-2.avif)

### Meshes

Components can be inserted on Meshes under the <span class="text-green-500 dark:text-green-400">green triangle</span> data icon.

![Mesh Panel](/images/the-blender-addon/mesh-panel.avif)

This can be important when inserting Components that require being inserted on Entitys with Mesh data to operate, such as Avian's [`ColliderConstructor::TrimeshFromMesh`](https://docs.rs/avian3d/latest/avian3d/collision/collider/enum.ColliderConstructor.html#variant.TrimeshFromMesh) which constructs a collider from mesh data.

> [!IMPORTANT]
> Components on Meshes and Materials are often applied to the same Entity in Bevy. This means Components on Meshes and Materials can "collide" and one will overwrite the other if you use the same Component on each.

### Materials

Components can be inserted on Meshes under the <span class="text-red-500 dark:text-red-400">red sphere</span> material icon.

![Material Panel](/images/the-blender-addon/material-panel.avif)

![UseGoalMaterial](/images/the-blender-addon/use-goal-material.avif)
