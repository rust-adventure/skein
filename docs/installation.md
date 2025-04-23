---
title: Installation
description: Installing the Bevy Plugin and the Blender addon
opengraph_image: /opengraph/opengraph-installation.jpg
---

There are two pieces to Skein:

1. The Bevy crate
2. The Blender addon

---

## The Bevy Crate

```shell
cargo add bevy_skein
```

Add the plugin to your application. Using `default` sets `handle_brp` to `true` which lets Skein set up the appropriate BRP configuration.
If you want more control, set this to `false` (or disable `default-features`) and set up the `RemotePlugin` and `RemoteHttpPlugin` yourself.
Skein currently only uses the default ports and disables BRP on wasm.

```rust
use bevy::prelude::*;
use bevy_skein::SkeinPlugin;

fn main() {
    App::new()
        .add_plugins((
            DefaultPlugins,
            SkeinPlugin::default(),
        ))
        .run();
}
```

The only thing you need to do is set up the plugin.
Skein operates on the `GltfExtras` that the Blender addon sets up in the .gltf/.glb file, so spawning a scene from a `.gltf` exported with the addon data will "just work".

```rust
commands.spawn(SceneRoot(asset_server.load(
    GltfAssetLabel::Scene(0).from_asset("my_export.gltf"),
)));
```

---

## The Blender addon

### Auto-Update Installation

The "auto-update" installation will use the "Static Registry" hosted on this website to check for extension updates when Blender starts up. This makes it easy to stay up to date.

1. Drag [this link](/releases/bevy_skein-0.1.6-dev.zip?repository=.%2Findex.json) onto Blender to add the registry
1. Accept the dialog that pops up (TODO)
1. Navigate to extensions and search for "bevy skein" which will now appear with an install button

Using this method, the registry will be checked for updates and allow you to update through Blender without downloading additional zip files.

### Manual Installation

Using manual installation will lock your installation to the version you download with the zip file.
It will be your responsibility to keep it up to date.
This is also a viable install strategy for local development.

1. Download the zip file from the latest [blender addon release](https://github.com/rust-adventure/skein/releases) on GitHub
2. Open Blender, navigate to `Edit -> Add-ons`
   ![addons](/images/docs/installation/addons.avif)
3. Drag .zip file onto addons list and "Install from Disk"
   ![install from disk](/images/docs/installation/install-addon.avif)
4. Bevy Skein should be installed in the list
   ![bevy_skein is installed](/images/docs/installation/bevy-skein-installed.avif)

### Addon Preferences

> [!Tip]
>
> There is a debug option in the addon preferences. If you want to develop against the addon you can enable this to see a bunch of output (note: requires running Blender from terminal)

![debug preferences](/images/docs/installation/debug-preferences.avif)
