---
title: Bevy Remote Protocol
description: Quidem magni aut exercitationem maxime rerum eos.
---

The [Bevy Remote Protocol](https://docs.rs/bevy/latest/bevy/remote/index.html) (**BRP**) is a JSON-RPC protocol designed to allow the remote access to a Bevy application.

Skein uses **BRP** over HTTP to fetch the Bevy registry of type information for your Bevy application. This is the information that powers the ability to select Components and insert them onto Objects in the Blender addon.

Skein will set up the remote plugin and an http server for you (or you can do it yourself). The Blender addon will then fetch this information any time you run the `Fetch Bevy Type Registry` Operator.

## An Example Response

Here's a `Player` struct with some fields:

```rust
#[derive(Component, Reflect, Debug)]
#[reflect(Component)]
pub struct Player {
    pub name: String,
    pub power: f32,
    pub test: i32,
}
```

The relevant subset of the API response looks like this. This is the data we use to build the Blender addon's Component forms.

```json
{
  "i32": {
    "kind": "Value",
    "reflectTypes": ["Default", "Serialize", "Deserialize"],
    "shortPath": "i32",
    "type": "int",
    "typePath": "i32"
  },
  "f32": {
    "kind": "Value",
    "reflectTypes": ["Default", "Serialize", "Deserialize"],
    "shortPath": "f32",
    "type": "float",
    "typePath": "f32"
  },
  "alloc::string::String": {
    "crateName": "alloc",
    "kind": "Value",
    "modulePath": "alloc::string",
    "reflectTypes": ["Default", "Serialize", "Deserialize"],
    "shortPath": "String",
    "type": "string",
    "typePath": "alloc::string::String"
  },
  "component_tests::Player": {
    "additionalProperties": false,
    "crateName": "component_tests",
    "kind": "Struct",
    "modulePath": "component_tests",
    "properties": {
      "name": { "type": { "$ref": "#/$defs/alloc::string::String" } },
      "power": { "type": { "$ref": "#/$defs/f32" } },
      "test": { "type": { "$ref": "#/$defs/i32" } }
    },
    "reflectTypes": ["Component", "Serialize", "Deserialize"],
    "required": ["name", "power", "test"],
    "shortPath": "Player",
    "type": "object",
    "typePath": "component_tests::Player"
  }
}
```

## skein-registry.json

Once fetched, the Blender addon will store the registry information in a `Text` block named `skein-registry.json`.

You can navigate to the `Scripting` tab and view the `Blender File` in the `Outliner`. In this list _after you've fetched the Bevy Registry information_ you will see a `Texts` item with a `skein-registry.json` field that contains the registry information. This file is used to rebuild the Component types, enabling the .blend file to be distributed without worrying about whether a Bevy application is running or not.

![skein-registry.json](/images/the-blender-addon/skein-registry-json.avif)
