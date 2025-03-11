# Replace Material Example

![bevy application running](../documentation/replace_material_run.avif)

This example shows using a `Component`'s `on_add` hooks to replace materials defined in Blender when the Bevy application runs.

In Blender, a `Component` (`UseDebugMaterial` in this example) can be added to a Material.
Any object this Material is attached to will also have this `Component`.

![blender ui](../documentation/replace_material_blender.avif)

This `UseDebugMaterial` has an on_add hook that replaces the `StandardMaterial` with a Bevy handle to another material.

```rust
#[derive(Component, Reflect)]
#[reflect(Component)]
#[component(on_add = on_add_use_debug_material)]
struct UseDebugMaterial;

/// The on_add hook that will run when the component is
/// added when spawning the glTF scene.
fn on_add_use_debug_material(
    mut world: DeferredWorld,
    HookContext { entity, .. }: HookContext,
) {
    let debug_material =
        world.resource::<DebugMaterial>().0.clone();

    world
        .commands()
        .entity(entity)
        .insert(MeshMaterial3d(debug_material));
}
```

> [!TIP]  
> In this example we create and store the material handle in a `Resource` at startup, allowing us to re-use the handle as many times as needed. You could use a HashMap instead to handle many handles like this.

> [!CAUTION]  
> The demo shows that any mesh that hasn't been UV unwrapped will not have the texture applied. This shows in the .gltf file as a missing `TEXCOORD_0` field. `Suzanne` in the following example glTF data has it, and `rock` does not.

```rust
{
    "name":"Suzanne",
    "primitives":[
        {
            "attributes":{
                "POSITION":28,
                "NORMAL":29,
                "TEXCOORD_0":30
            },
            "indices":31,
            "material":0
        }
    ]
},
{
    "name":"rock",
    "primitives":[
        {
            "attributes":{
                "POSITION":32,
                "NORMAL":33
            },
            "indices":34,
            "material":0
        }
    ]
},
```
