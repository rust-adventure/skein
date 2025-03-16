//! An example that is only used to serve up Component
//! registry information in various ways that can be
//! tested in Blender
//!
//! it renders nothing, and only exists to serve BRP requests
//!
//! The file `./component_tests.json` is built from the BRP schema
//! this example provides and is the minimal set of types required
//! to reflect and construct values of the components registered here.
use bevy::prelude::*;
use skein::SkeinPlugin;
use test_components::*;

fn main() {
    App::new()
        .register_type::<Player>()
        .register_type::<TeamMember>()
        .register_type::<ATupleStruct>()
        .register_type::<Marker>()
        .register_type::<TaskPriority>()
        .register_type::<SomeThings>()
        .register_type::<MultiElementTupleStruct>()
        .register_type::<AnOptionalName>()
        .register_type::<NonZeroNumbers>()
        // below this line are types that aren't expected to work
        // for example: Components containing Timers
        .register_type::<TimerContainer>()
        .register_type::<BucketOfTypes>()
        .register_type::<RichAndUnitEnum>()
        // add plugins
        .add_plugins((
            DefaultPlugins,
            SkeinPlugin::default(),
        ))
        .run();
}
