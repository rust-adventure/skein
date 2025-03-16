skein is split into two major pieces:

- Rust crate (Bevy Plugin)
- Blender Addon (Python)

## Rust crate

The Rust crate is a Bevy plugin. Nothing special, just a Cargo.toml. `cargo test`, etc all work.

## Blender Addon

The Blender addon is written in Python and comes with the usual python requirements.

`__init__.py` is written in such a way that you can copy/paste the file into the a new scripting text file in the Blender Scripting tab, then run it. You don't have to install anything if you do this, but you won't be able to run tests.

## Testing

For more automated testing, I happen to be using [pipx](https://github.com/pypa/pipx) and [virtualenv](https://virtualenv.pypa.io), and [pyenv]()

```
brew install pipx pyenv
pipx ensurepath
pipx install virtualenv
pyenv install 3.10
# pyenv shims will show you the path to a python 3.10, which is
# required for bpy to install
pyenv shims
virtualenv skein-dev -p /Users/chris/.pyenv/shims/python3.10
source skein-dev/bin/activate
pip install bpy requests
pip install -U pytest
```

## The Python Dataflow

1. Registry data is fetched from a running bevy application via BRP
   - this data is cached in a file that lives inside the .blend file
     - this cache is used if it exists instead of making a fetch when opening a blend file, which allows editing Blender scenes without running a Bevy app.
2. the registry json data is converted into Blender PropertyGroup classes and a collection of component type_paths are stored for later use
3. the user selects an object, navigates to the Properties.object/.mesh/.material tab
4. the user uses a search field to pick a component
5. the user clicks a button that fires the InsertBevyComponent operator
   - the operator inserts the component onto the relevant object/mesh/materials's components collection
6. the component that is selected is shown as a form in the Properties.object panel using the PropertyGroup
7. once components are inserted and filled out with data, the user exports gltf however they want to
8. the skein export extension cleans up the data that was stored on objects and formats it so that Bevy can use the reflection data directly without modification
9. The user spawns a gltf scene in Bevy, which now hold the `GltfExtras`/`GltfMeshExtras`/`GltfMaterialExtras` we stored on the nodes when exporting
10. An observer reflects the component data from `GltfExtras`/`GltfMeshExtras`/`GltfMaterialExtras` onto the relevant nodes, instantiating all components applied in Blender

#### WindowManager

- registry
  - holds the json registry data as a string from the brp request
- components
  - a Collection of component data used for creating lists the user can select a component from
- skein_property_groups
  - The property groups created after fetching the registry data

#### Object

- skein
  - Collection of component data

##### ComponentData

- type_path
- name
- value

## Value types

There are "primitive" types in the Bevy reflection data that have a `kind` of `Value`, but do not have additional information about what values they contain. We can not build UI for these without hardcoding assumptions into the python addon. Some examples include

- third party types:
  - `smol_str::SmolStr`
- std or core types
  - `std::path::PathBuf`
- other Bevy types
  - `Entity`.
- avian's `TrimeshFlags`
  - a `bitfield!` stored in a u8 and `reflect(opaque)`

```json
{
  "smol_str::SmolStr": {
    "crateName": "smol_str",
    "kind": "Value",
    "modulePath": "smol_str",
    "reflectTypes": ["Default", "Serialize", "Deserialize"],
    "shortPath": "SmolStr",
    "type": "object",
    "typePath": "smol_str::SmolStr"
  },
  "std::path::PathBuf": {
    "crateName": "std",
    "kind": "Value",
    "modulePath": "std::path",
    "reflectTypes": ["Default", "Serialize", "Deserialize"],
    "shortPath": "PathBuf",
    "type": "object",
    "typePath": "std::path::PathBuf"
  },
  "bevy_ecs::entity::Entity": {
    "crateName": "bevy_ecs",
    "kind": "Value",
    "modulePath": "bevy_ecs::entity",
    "reflectTypes": ["Serialize", "Deserialize"],
    "shortPath": "Entity",
    "type": "object",
    "typePath": "bevy_ecs::entity::Entity"
  }
}
```

## Interesting Future Work

- Can we add any reflected `Default` data to the registry information and use that in Blender for default values?
- Relationships: How can we support a good Blender UI for assigning custom Bevy Relationships
- If a variant of a complex enum is not constructible, what happens? can we just drop the non-constructible one? or render a note in the UI

## TODO:

- Write developing documentation
- Write end-user documentation/how to use
- DistanceFog forms show uneditable content (check if this is still true)
- Some/None UI shows everything
- make_property for Enums with unit variants that aren't Option

### Edge Cases to add tests for

- How does it handle 6-level nested structs?
- glam Values (and other values)

---

- How to drive component values for instanced objects?
- Clear skein-registry.json when fetching new bevy reflection data.
