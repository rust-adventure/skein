# Blender Addon Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

- [Support type_paths > 63 characters long](https://github.com/rust-adventure/skein/issues/1), like `avian3d::dynamics::rigid_body::mass_properties::components::Mass`
- implement default values for Maps and Lists, which will export as {} and []. This enables some types, like ColliderConstructorHierarcy from Avian, which have HashMaps that aren't used but need to be handled.
- Many glam types are now explicitly handled in the UI, making them easier to associate with headings and inner properties, like knowing an x,y and z are related.
-

### Dev changes

- touch all PropertyGroups when inserting new data, as this is required to make data that is uninitialized accessible to the first render. We use introspection on the python types, so the values must be forcibly initialized.
- rewrite implementation of UI rendering. The implementation is now simpler and uses fewer sources of information.

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

[unreleased]: https://github.com/rust-adventure/skein/compare/blender-v0.1.3...HEAD
[0.1.3]: https://github.com/rust-adventure/skein/compare/blender-v0.1.3...blender-v0.1.3
[0.1.2]: https://github.com/rust-adventure/skein/compare/blender-v0.1.1...blender-v0.1.2
[0.1.1]: https://github.com/rust-adventure/skein/compare/blender-v0.1.0...blender-v0.1.1
[0.1.0]: https://github.com/rust-adventure/skein/releases/tag/blender-v0.1.0
