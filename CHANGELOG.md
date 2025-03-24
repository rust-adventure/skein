# Blender Addon Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

## [0.1.2] - 2025-03-24

- [Correctly serialize nested enum values](https://github.com/rust-adventure/skein/issues/6)
- [Serialize Vec3 as an array instead of an object](https://github.com/rust-adventure/skein/issues/4)
  - Vec3's serialization is an array which is different than its type registry data. This is also true for other types, which will be fixed in a future release.
- [Clear old components when fetching new Bevy registry data](https://github.com/rust-adventure/skein/issues/7)
  - Allows updating components to add fields without closing Blender

## [0.1.1] - 2025-03-22

- Enable ability to override library assets' component data when instancing from separate blend files

## [0.1] - 2025-03-17

Initial Release of Blender Addon

[unreleased]: https://github.com/rust-adventure/skein/compare/blender-v0.1.2...HEAD
[0.1.2]: https://github.com/rust-adventure/skein/compare/blender-v0.1.0...blender-v0.1.1
[0.0.1]: https://github.com/rust-adventure/skein/releases/tag/blender-v0.1.0
