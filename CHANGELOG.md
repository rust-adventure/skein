# Blender Addon Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

- Add custom BRP methods in `Plugin::finish`, which enables users to configure their own BRP host/port and plays nicely with other crates which may add methods of their own
- Don't attempt to use `brp` feature or `dep:bevy_remote` on wasm

- New `debug` logs in the skein plugin enable showing whether skein is controlling the BRP plugins or not, as well as if skein is adding additional endpoints. These aren't shown by default, so you have to enable them if you want them:

```
❯ RUST_LOG=info,bevy_skein=debug bevy run --example components_on_bone
DEBUG build: bevy_skein: adding `bevy_remote::RemotePlugin` and `bevy_remote::http::RemoteHttpPlugin`. BRP HTTP server running at: 127.0.0.1:15702
DEBUG bevy_skein: enabling skein/presets endpoint
```

## [0.3.0]

- Bevy 0.17 support
- [#61](https://github.com/rust-adventure/skein/pull/61): Only enable BRP in dev builds by default using `cfg!(debug_assertions)` for `handle_brp` in the `Default` implementation of `SkeinPlugin`.

## [0.2.0-rc.3]

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

## [0.2.0-rc.2] - 2025-04-14

- Disable wasm by default
- Put bevy_remote behind a `brp` feature, which is enabled by default

## [0.2.0-rc.1] - 2025-03-23

Bevy 0.16-rc compatible release

## [0.1.x] - 2025-03-13

Initial Release of Rust crate. Compatible with Bevy 0.15

[unreleased]: https://github.com/rust-adventure/skein/compare/v0.1.5...HEAD
[0.2.0-rc.3]: https://github.com/rust-adventure/skein/compare/v0.2.0-rc.2...v0.2.0-rc.3
[0.1.x]: https://github.com/rust-adventure/skein/releases/tag/v0.1.0
