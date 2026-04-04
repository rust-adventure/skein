//! make sure SkeinPlugin options are all
//! publically setable if they should be, and that
//! the plugin constructs without issue

use bevy_gltf::GltfPlugin;
#[test]
fn test_skein_options() {
    use bevy::prelude::*;
    use bevy_skein::SkeinPlugin;

    App::new()
        .add_plugins((
            MinimalPlugins,
            AssetPlugin::default(),
            GltfPlugin::default(),
            SkeinPlugin { handle_brp: false },
        ))
        // immediately exit
        .add_systems(
            Startup,
            |mut exit_event: MessageWriter<AppExit>| {
                exit_event.write(AppExit::Success);
            },
        )
        .run();
}
