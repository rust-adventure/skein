---
title: Quickstart
description: A starter template for a new Bevy + Skein application
opengraph_image: /opengraph/opengraph-quickstart.jpg
---

Using either the [Bevy CLI](https://github.com/thebevyflock/bevy_cli) or [`cargo-generate`](https://cargo-generate.github.io/cargo-generate/) you can scaffold a new Bevy application with Skein pre-installed and a .gltf file ready to go.

## Bevy 0.17 (stable)

Using the [Bevy CLI](https://github.com/thebevyflock/bevy_cli) (currently under development):

```shell
bevy new -t rust-adventure/skein --branch template-minimal my-newest-project
```

Using [`cargo generate`](https://cargo-generate.github.io/cargo-generate/):

```shell
cargo install cargo-generate
cargo generate rust-adventure/skein --branch template-minimal --name my-new-project
```
