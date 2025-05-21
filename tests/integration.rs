//! make sure SkeinPlugin options are all
//! publically setable if they should be, and that
//! the plugin constructs without issue
#[test]
fn test_skein_options() {
    use bevy::prelude::*;
    use bevy_skein::SkeinPlugin;

    App::new()
        .add_plugins((
            MinimalPlugins,
            SkeinPlugin {
                handle_brp: false,
                ..default()
            },
        ))
        // immediately exit
        .add_systems(
            Startup,
            |mut exit_event: EventWriter<AppExit>| {
                exit_event.write(AppExit::Success);
            },
        )
        .run();
}
