# Skein Docs

The Skein site is a [Cinnog] App. Cinnog is a static site generator using [Leptos] with Bevy ECS as a data layer.

- `cargo make serve` serves the App with watch mode and hot-reload enabled.
- `cargo make build` builds the project in release. The output will be in the `dist` directory and the command will not serve it, but quit instead.
- `cargo make fmt` formats with `rustfmt` and `leptosfmt`.
- `cargo make e2e` runs the end-to-end tests from the `end2end` directory using [Playwright].

## The Data layer

[Bevy ECS] is used in an attempt to add a data layer to Leptos as a static site generator. The idea is similar to what Gatsby does with GraphQL using a Bevy ECS World as an in-memory database. The API of Bevy ECS is very nice to work with as a user. It removes any need of an extra syntax for data queries.

[Cinnog] is quite minimal at the moment and very experimental. In `generator`, a new data layer is constructed and filled with example data from markdown and `ron` files.

When all data is loaded and processed, Cinnog can build a given Leptos app and will supply the data layer in a context. Inside components, you can run [Systems][bevy_systems] against the data layer (think GraphQL query in Gatsby) and use [Resources][bevy_resources].

## License

Dual-licensed under either of

- Apache License, Version 2.0, ([LICENSE-APACHE](/LICENSE-APACHE) or https://www.apache.org/licenses/LICENSE-2.0)
- MIT license ([LICENSE-MIT](/LICENSE-MIT) or https://opensource.org/licenses/MIT)

at your option.

## Contribution

Unless you explicitly state otherwise, any contribution intentionally submitted
for inclusion in the work by you, as defined in the Apache-2.0 license, shall be dual licensed as above, without any
additional terms or conditions.

[bevy_systems]: https://bevy-cheatbook.github.io/programming/systems.html?highlight=system#systems
[bevy_resources]: https://bevy-cheatbook.github.io/programming/res.html
[Bevy ECS]: https://github.com/bevyengine/bevy/tree/main/crates/bevy_ecs
[Leptos]: https://github.com/leptos-rs/leptos
[Cinnog]: https://github.com/NiklasEi/cinnog
[Playwright]: https://playwright.dev/
