# Replace Material Example

![bevy application running](../documentation/replace_material.avif)

This example shows using a `Component`'s `on_add` hooks to replace materials defined in Blender when the Bevy application runs.

In Blender, a `Component` (`UseDebugMaterial` or `UseForceField` in this example) can be added to a Material.
Any object this Material is attached to will also have this `Component`.

![blender ui](../documentation/replace_material_blend.avif)

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
        world.resource::<MaterialStore>().debug.clone();

    world
        .commands()
        .entity(entity)
        .insert(MeshMaterial3d(debug_material));
}
```

> [!TIP]  
> In this example we create and store the material handle in a `Resource` at startup, allowing us to re-use the handle as many times as needed. You could use a HashMap instead to handle many handles like this or ignore it completely and recreate the material if you don't care.

> [!CAUTION]  
> Any mesh that hasn't been UV unwrapped may seem like it isn't working. This shows up in .gltf files as a missing `TEXCOORD_0` field. `Suzanne` in the following example glTF data has it, and `rock` does not. This is something you can check for in Blender.

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
