# Blender Addon Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

## [0.1.11]

- The extension will now work with Bevy 0.16 and 0.17 applications.
  Note that some type paths for core bevy types or third party crates might have changed between these two versions so be aware of that if you're upgrading.

- Remove the default registry, which would now be incorrect depending on which Bevy version you were using.

## [0.1.10]

Enable placing components on Blender Scene objects

## [0.1.9]

Enable placing components on individual bones

## [0.1.8]

bugfix: #38. Scalar components with type_paths over length 63 failed to export. This affected components like `avian3d::dynamics::rigid_body::mass_properties::components::Mass`.

## [0.1.7]

Fail gracefully if the skein/presets endpoint fails for any reason.

## [0.1.6]

### The First CLI Command

Introduces the first CLI command, `dump_component_data`, which can be used on the CLI to create a json file of all of the component usage in a blend file. All CLI commands are considered experimental as we research and build workflows, but this one doesn't mutate anything so is generally safe to run.

```
blender --background -b replace_material.blend -c dump_component_data -o test.json
```

### Presets

In addition to the support in the Rust crate, The Blender addon now supports reading Default implementation values and user-provided presets from Bevy applications. This means users can apply "default" or custom "preset" values inside of Blender.

These presets are one-off. There is no special storage for them once they are applied, they simply set the values that can be set, which is the same behavior you'd see if you set the values manually.

## [0.1.5] - 2025-04-11

- [Support type_paths > 63 characters long](https://github.com/rust-adventure/skein/issues/1), like `avian3d::dynamics::rigid_body::mass_properties::components::Mass`
- implement default values for Maps and Lists, which will export as {} and []. This enables some types, like ColliderConstructorHierarcy from Avian, which have HashMaps that aren't used but need to be handled.
- Many glam types are now explicitly handled in the UI, making them easier to associate with headings and inner properties, like knowing an x,y and z are related.
- opening a project or creating a new one will now _create_ a local skein-registry.json if one doesn't exist
- The `DebugCheckObjectBevyComponents` operator was removed from the edit menu. It still exists, but if you want it you'll have to call it directly or bind it to a key
- Operators for inserting are now per-object and can be bound to keymaps. Future work will likely introduce a generalized operator for hotkey insertion
- Add support for Cameras, Lights, and Collections

### Dev changes

- touch all PropertyGroups when inserting new data, as this is required to make data that is uninitialized accessible to the first render. We use introspection on the python types, so the values must be forcibly initialized.
- rewrite implementation of UI rendering. The implementation is now simpler and uses fewer sources of information.
- additional unregistration logic was added to .unregister
- Running headless blender/python tests now report when the registry.json file is missing and what to do about it
- add poll methods to as much as possible

## [0.1.3] - 2025-03-24

- [Implement glam's special serialization](https://github.com/rust-adventure/skein/issues/4) (arrays instead of objects for Vec2/3/4/affine/matrix)

## [0.1.2] - 2025-03-24

- [Correctly serialize nested enum values](https://github.com/rust-adventure/skein/issues/6)
- [Serialize Vec3 as an array instead of an object](https://github.com/rust-adventure/skein/issues/4)
  - Vec3's serialization is an array which is different than its type registry data. This is also true for other types, which will be fixed in a future release.
- [Clear old components when fetching new Bevy registry data](https://github.com/rust-adventure/skein/issues/7)
  - Allows updating components to add fields without closing Blender

## [0.1.1] - 2025-03-22

- Enable ability to override library assets' component data when instancing from separate blend files

## [0.1.0] - 2025-03-17

Initial Release of Blender Addon

[unreleased]: https://github.com/rust-adventure/skein/compare/blender-v0.1.9...HEAD
[0.1.9]: https://github.com/rust-adventure/skein/compare/blender-v0.1.8...blender-v0.1.9
[0.1.8]: https://github.com/rust-adventure/skein/compare/blender-v0.1.7...blender-v0.1.8
[0.1.7]: https://github.com/rust-adventure/skein/compare/blender-v0.1.6...blender-v0.1.7
[0.1.6]: https://github.com/rust-adventure/skein/compare/blender-v0.1.5...blender-v0.1.6
[0.1.5]: https://github.com/rust-adventure/skein/compare/blender-v0.1.3...blender-v0.1.5
[0.1.3]: https://github.com/rust-adventure/skein/compare/blender-v0.1.2...blender-v0.1.3
[0.1.2]: https://github.com/rust-adventure/skein/compare/blender-v0.1.1...blender-v0.1.2
[0.1.1]: https://github.com/rust-adventure/skein/compare/blender-v0.1.0...blender-v0.1.1
[0.1.0]: https://github.com/rust-adventure/skein/releases/tag/blender-v0.1.0
