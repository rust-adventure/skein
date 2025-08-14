---
title: Components as APIs
description: Defining and using Components via Reflection is basically the same as defining an API schema
opengraph_image: /opengraph/opengraph-components-as-apis.jpg
---

Once you start using Component definitions outside of Bevy you've opted into having clients for the API that those Components define.

You can choose to break the API contract or not depending on how important it is to you.
This page is intended to give you the information you need to make your own choices about how and when to break those APIs.

## Why are Components APIs?

A tldr; explanation is that:

- Components are the API schema
- The .blend file is your database
- .gltf/.glb exports are the queries clients have made against that data

Given a Component as such:

```rust
struct Player {
    name: String,
    power: i32,
    has_team: bool
}
```

The "API definition" can be thought of roughly as a SQL table.
Suppose you've used this component a number of times in Blender, creating a number of players in scenes.

| name  | power | has_team |
| ----- | ----- | -------- |
| Chris | 23    | true     |
| Lex   | 42    | false    |

Once we frame it as a database schema, those with database experience will immediately notice why this is a potential issue.

---

## An Example Change

To make it concrete, let's image a potential API change.
Let's say `has_team` is no longer serving our needs and we want to label the specific team the `Player` is on using an enum.

```rust
struct Team {
    Red,
    Green,
    Blue,
}

struct Player {
    name: String,
    power: i32,
    team: Team::Blue
}
```

The changes here include:

- removing the `has_team` field
- Adding the `team` field

If we examine our table now with these changes, the `has_team` column is being dropped and we don't know how to construct a value when one doesn't exist for `team`.

| name  | power | ~~has_team~~ | team |
| ----- | ----- | ------------ | ---- |
| Chris | 23    | ~~true~~     | ?    |
| Lex   | 42    | ~~false~~    | ?    |

The .blend file components will still contain the old data, but it won't be readable without knowing the fields exist, so if we make this change, we lock ourselves out from being able to read `has_team`.

We also can't construct this new Component type from the original data: we don't know how to construct a team!
So any .gltf files we've already exported that contain the original data don't contain enough data to load into the Bevy application that uses the new Component type.

So how do we deal with this? We can fix these issues or ignore them entirely!
Its up to you.
If you still want to use the data, even for migrating, then keep the fields around until you no longer need the data.

The fundamental rule to understand is that if you remove types from your Component definition the affected fields' data becomes inaccessible in Blender.
If you don't care about the data, then continue as normal and re-export your gltf files. Everything will still work.

If you work in a larger team, perhaps with many blend files across many users.
Or if you want to provide types that users can use to build their own levels, then you'll need to care more about the changes you make.

---

## Forward and Backward compatibility

Schema design and evolution is a large topic.
Thankfully any resource you find that talks about concepts like forward and backward compatibility in schema design will apply here.

**Forward compatibility** ensures that newer schema users in Blender can write data that old schema consumers (old Bevy App versions) can still read.

An example of this would be a Component change that included new fields without modifying old ones.
An old Bevy App built with an old schema (say, a released version of a game) would be able to read a new gltf file that used the new schema because the new field data doesn't break anything and can be dropped.

**Backward compatibility** means that old gltf files can be loaded by newer Bevy applications with newer schemas.

An example of this is the addition of a field that has a default value. Old schema Blender users will continue to not know or use the new field, New schema Blender users will write values.
When a gltf file that is written out by either user is read, the new schema will work as expected, while the old schema will result in using the Default value for the new field.

Decide which is important to you, if either at all.

## Modifications to Components

You have full agency over the approach you use. Here's a few use cases

### Splitting a Component in Two

Lets take the example before of a `Player` Component with `name`, `power`, and `team` fields.

```rust
#[derive(Component, Reflect)]
#[reflect(Component)]
struct Team {
    Red,
    Green,
    Blue,
}

#[derive(Component, Reflect)]
#[reflect(Component)]
struct Player {
    name: String,
    power: i32,
    team: Team::Blue
}
```

It really seems like the `team` field should be its own component so let's make it one.

Its fairly obvious that we would make the `Team` enum a Component as well but what we do with the `team` field depends on our use case.

If we remove the `team` field immediately, we lose access to that data in Blender. If you're ok with re-inserting that data or otherwise don't need it that's fine.

If you want to keep that data and move it into the new Component, then it becomes a multi-step process.

1. Make `Team` a Component, and leave the `team` field as is
2. In Blender, for any Component that uses the `team` field, insert the new the `Team` Component using the `team` field data as a reference
3. Once the data has been migrated, remove the `team` field.

This allows you full access to the existing data while migrating to the new usage, and lets you remove the old field in the end.

## Controlling the type_path

If you find yourself moving Components around, or want a more explicit set of Components to use in Blender, you can control two important aspects of the Reflection implementation:

- `type_path`
- `type_name`

The `type_path` is the module path.
Using the `type_path` attribute, you can define the way this module path will show up when using it inside of Blender, no matter where it is in your source code.
Similarly, `type_name` is the name Reflection will use.

Here's an example.
Normally in Blender and other Reflection use cases you'd use this component as `path::to::module::Character`.
With our changes, this Component will show up as `api::Something` in Blender regardless of where it is in our source code.

```rust
#[derive(Component, Reflect, Debug)]
#[reflect(Component)]
#[type_path = "api"]
#[type_name = "Something"]
struct Character {
    name: String,
}
```

You'll be able to use it in source code as `Character` while using it in Blender as `Something`.
This allows you to rename and move the Component around at-will without making changes in Blender.
