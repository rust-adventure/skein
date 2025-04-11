---
title: Mark and Modify Blender Objects, Materials, and Meshes
description: Using Component Hooks, Observers, or even regular systems in addition to inserted Components in Blender, we can modify entities directly, whenever we want.
opengraph_image: /opengraph/opengraph-mark-and-modify-blender-objects.jpg
---

When Components are inserted onto an Entity, such as the ones we've defined in Blender, Hook and Observer events will fire and allow us to write code that runs in reaction.

## Hooks

Bevy's [Component Hooks](https://docs.rs/bevy/0.16.0-rc.3/bevy/prelude/trait.Component.html#adding-components-hooks) run basically immediately when a Component is added to an `Entity`. It is possible to define at least the following hooks for a Component:

- `on_add`
- `on_insert`
- `on_replace`
- `on_remove`
- `on_despawn`

A practial use case for hooks is shown in [Replace a Blender Material](/docs/replace-a-blender-material).

Defining a hook can be done via attribute macro:

```rust
#[derive(Component, Reflect)]
#[reflect(Component)]
#[component(on_add = on_add_use_force_field_material)]
struct UseForceFieldMaterial;
```

Its notable that the hook function has a different signature than the systems you might be more used to writing, and things like `commands` need to be accessed via the `DeferredWorld`.

```rust
fn on_add_use_force_field_material(
    mut world: DeferredWorld,
    HookContext { entity, .. }: HookContext,
) {
    let force_field = world
        .resource::<MaterialStore>()
        .force_field
        .clone();

    world
        .commands()
        .entity(entity)
        .remove::<MeshMaterial3d<StandardMaterial>>()
        .insert(MeshMaterial3d(force_field));
}
```

## Observers

[Observers](https://docs.rs/bevy/0.16.0-rc.3/bevy/ecs/observer/struct.Observer.html) can react to more events than hooks and are thus more flexible. Observers run just after Hooks.

Similar to Hooks, Observers can trigger on many of the same events:

- [`OnAdd`](https://docs.rs/bevy/0.16.0-rc.3/bevy/ecs/prelude/struct.OnAdd.html)
- [`OnInsert`](https://docs.rs/bevy/0.16.0-rc.3/bevy/ecs/prelude/struct.OnInsert.html)
- [`OnRemove`](https://docs.rs/bevy/0.16.0-rc.3/bevy/ecs/prelude/struct.OnRemove.html)
- [`OnReplace`](https://docs.rs/bevy/0.16.0-rc.3/bevy/ecs/prelude/struct.OnReplace.html)
- [`OnDespawn`](https://docs.rs/bevy/0.16.0-rc.3/bevy/ecs/world/struct.OnDespawn.html)

A global observer can be added at the `App` level.

```rust
App::new()
    .add_observer(on_add_force_field)
    .run()
```

and Observers look a lot more like regular systems.

```rust
fn on_add_force_field(
    trigger: Trigger<OnAdd, UseForceFieldMaterial>,
    mut commands: Commands,
    material_store: Res<MaterialStore>,
) {
    let force_field = material_store
        .force_field
        .clone();

    commands
        .entity(trigger.target())
        .remove::<MeshMaterial3d<StandardMaterial>>()
        .insert(MeshMaterial3d(force_field));
}
```
