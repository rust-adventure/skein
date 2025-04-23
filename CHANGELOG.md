# Blender Addon Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Presets

Many Components have Default implementations but those aren't the only "pre-configured values" a user might want to apply. This release introduces a new BRP endpoint that is enabled by default and queried by the Blender addon. The BRP endpoint `skein/presets` builds all `Default` values for all applicable Components, as well as user-provided presets.

Users can provide presets using the `insert_skein_preset` API, which allows setting them near the `register_type` invocations.

```rust
fn main() {
    App::new()
        .register_type::<TeamMember>()
        .insert_skein_preset("Luigi", TeamMember {
            player: Player {
                name: "Luigi Mario".to_string(),
                power: 100.,
                test: 5
            },
            team: Team::Green,
        })
    ...
}
```

## [0.2.1-rc.2] - 2025-04-14

- Disable wasm by default
- Put bevy_remote behind a `brp` feature, which is enabled by default

## [0.2.1-rc.1] - 2025-03-23

Bevy 0.16-rc compatible release

## [0.1.x] - 2025-03-13

Initial Release of Rust crate. Compatible with Bevy 0.15

[unreleased]: https://github.com/rust-adventure/skein/compare/blender-v0.1.5...HEAD
[0.1.5]: https://github.com/rust-adventure/skein/compare/blender-v0.1.3...blender-v0.1.5
[0.1.3]: https://github.com/rust-adventure/skein/compare/blender-v0.1.2...blender-v0.1.3
[0.1.2]: https://github.com/rust-adventure/skein/compare/blender-v0.1.1...blender-v0.1.2
[0.1.1]: https://github.com/rust-adventure/skein/compare/blender-v0.1.0...blender-v0.1.1
[0.1.0]: https://github.com/rust-adventure/skein/releases/tag/blender-v0.1.0
