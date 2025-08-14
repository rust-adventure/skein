---
title: Inserting Components
description: How to insert Bevy components in Blender using the Skein addon
opengraph_image: /opengraph/opengraph-inserting-components.jpg
---

_After_ [fetching the **Bevy Type Registry**](/docs/fetching-the-bevy-type-registry) information; **Components** can be inserted on Blender **Objects**, **Meshes**, **Materials**, **Scenes**, **Lights**, **Collections**, and **Bones**.

After selecting an **Object**, the UI for this exists in the **Properties** area in the **Object** tab. You may need to scroll down to see the **Skein Bevy Panel**.

In the **Skein Bevy Panel**, there's an empty field labelled `type:`.

![Object Panel](/images/the-blender-addon/object-panel.avif)

This field will autocomplete on the full `type_path` for all applicable Components.

![Inserting Component](/images/the-blender-addon/inserting-component.avif)

Once you choose a Component's `type_path`, the component must be inserted using the Button below labelled **Insert Component Data**.

![Inserted Component](/images/the-blender-addon/inserted-component.avif)

After inserting Components, selecting any component in the list allows you to edit the relevant values, if there are any.

![Editing Component](/images/the-blender-addon/editing-component.avif)

Unit structs, such as Marker components, will show a message stating that there isn't any data to modify.

![Marker Components](/images/the-blender-addon/marker-components.avif)

---

## Objects, Meshes, and Materials

Objects, Meshes, etc are all located in slightly different places in the Blender UI and all of them can receive components.

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

### Scenes

Components can be inserted on Scenes under the <span class="text-gray-500 dark:text-gray-400">gray</span> scene items icon.

![Scene Panel](/images/introduction/panel-scene.avif)

### Lights

Components can be inserted on Lights under the <span class="text-green-500 dark:text-green-400">green light</span> icon.

![Light Panel](/images/introduction/panel-light.avif)

### Bones

Components can be inserted on Bones under the <span class="text-green-500 dark:text-green-400">green bone</span> icon.

This is slightly different from the other panels, in that if you select the bone in the outliner, it will change which bone you're adding Components to, so pay attention to which bone is selected!

![Bone Panel](/images/introduction/panel-bone.avif)

### Collections

Components can be inserted on Collections under the <span class="text-gray-500 dark:text-gray-400">gray box</span> collection icon.

> [!NOTE]
> Collections are eliminated in Blender's default export configuration! You _probably_ don't want to enable the additional hierarchy nodes, but it is supported if you do.

![Collection Panel](/images/introduction/panel-collection.avif)
