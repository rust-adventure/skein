---
title: Reflection
description: What is Reflection in Bevy and how is it useful to Skein
opengraph_image: /opengraph/opengraph-reflection.jpg
---

Skein uses Bevy's Reflection infrastructure to be able to know what Components can be inserted in Blender, as well as turning those values into realized Components when your Bevy app runs.

At its core, reflection allows us to inspect the program itself, its syntax, and its type information at runtime.
The documentation for [`bevy_reflect`](https://docs.rs/bevy/latest/bevy/reflect/index.html) details a number of traits that enable a variety of use cases.

Here is

```rust
#[derive(Component, Reflect, Default)]
#[reflect(Component, Default)]
#[type_path = "blender"]
#[type_name = "Player"]
struct MyComponent {
    name: String,
    team: String
}
```

Skein's usage of Reflection comes in two major forms:

- Reading the [TypeRegistry](https://docs.rs/bevy/0.16.1/bevy/reflect/struct.TypeRegistry.html) and sending relevant metadata about the types in a Bevy app to Blender
- Taking json-style Component data and instantiating it using reflection

## Inserting Reflected Data

Skein's implementation for turning a JSON value into a Component inserted on an Entity boils down to

- reading the type registry
- deserializing the JSON component data using the information in the type registry
- inserting that data as a Component

```rust
let type_registry = type_registry.read();

let reflect_deserializer = ReflectDeserializer::new(&type_registry);
let reflect_value = reflect_deserializer.deserialize(json_component).unwrap()

commands
    .entity(entity)
    .insert_reflect(reflect_value);
```

## Caveats

If a Component uses a custom serde Serialization, that is not represented in the type registry metadata.
This is also true for types like Vec3 in the `glam` crate, but since these types are so important, they are implemented manually.
