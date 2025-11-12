#![doc = include_str!("../README.md")]
use bevy_app::{App, Plugin};
use bevy_ecs::{
    name::Name,
    observer::On,
    prelude::Add,
    reflect::{AppTypeRegistry, ReflectCommandExt},
    resource::Resource,
    system::{Commands, Query, Res},
};
use bevy_gltf::{
    GltfExtras, GltfMaterialExtras, GltfMeshExtras,
    GltfSceneExtras,
};
use bevy_log::{debug, error, trace};
use bevy_platform::collections::HashMap;
use bevy_reflect::{Reflect, serde::ReflectDeserializer};
use serde::de::DeserializeSeed;
use serde_json::Value;
use tracing::{instrument, warn};

/// Presets provide defaults and preset
/// configurations of values from Bevy to Blender.
/// Enabling using `Default` implementations when
/// inserting Components in Blender.
/// In Bevy, this module enables the BRP endpoint
/// that serves up the Default and user-provided
/// preset values.
#[cfg(all(
    not(target_family = "wasm"),
    feature = "presets"
))]
pub mod presets;

/// [`SkeinPlugin`] is the main plugin.
///
/// This will add Scene postprocessing which will
/// introspect glTF extras and set up the expected
/// components using Bevy's reflection
/// infrastructure.
pub struct SkeinPlugin {
    /// Whether Skein should handle adding the
    /// Bevy Remote Protocol plugins.
    ///
    /// Use `false` if you want to handle setting
    /// up BRP yourself. The default constructor will
    /// only enable BRP in dev builds.
    #[allow(dead_code)]
    pub handle_brp: bool,
}

impl Default for SkeinPlugin {
    fn default() -> Self {
        let dev = cfg!(debug_assertions);
        Self { handle_brp: dev }
    }
}

impl Plugin for SkeinPlugin {
    #[instrument(skip(self, app))]
    fn build(&self, app: &mut App) {
        app.init_resource::<SkeinPresetRegistry>()
            .add_observer(skein_processing);

        // If we're not on wasm, and the brp feature
        // is enabled, check for whether the user wants
        // skein to handle setting up BRP or not.
        //
        // The `handle_brp` default is to enable `brp`
        // and skein's custom endpoints when `debug_assertions`
        // are enabled. This is mostly the difference
        // between `dev` and `release`, but can be configured
        // by users as well.
        #[cfg(all(
            not(target_family = "wasm"),
            feature = "brp"
        ))]
        if self.handle_brp {
            debug!(
                "adding `bevy_remote::RemotePlugin` and `bevy_remote::http::RemoteHttpPlugin`. BRP HTTP server running at: {}:{}",
                bevy_remote::http::DEFAULT_ADDR,
                bevy_remote::http::DEFAULT_PORT
            );
            app.add_plugins((
                // We only add the defaults. If a user wants 
                // a different configuration, they can set 
                // the plugins up themselves.
                bevy_remote::RemotePlugin::default(),
                bevy_remote::http::RemoteHttpPlugin::default(),
            ));
        } else {
            debug!(
                "Skein is *not* adding `RemotePlugin` and `RemoteHttpPlugin`"
            );
        }
    }

    #[cfg(all(
        not(target_family = "wasm"),
        feature = "brp"
    ))]
    #[instrument(skip(self, app))]
    fn finish(&self, app: &mut App) {
        {
            // add presets endpoint
            #[cfg(feature = "presets")]
            {
                debug!(
                    "enabling {} endpoint",
                    presets::BRP_SKEIN_PRESETS_METHOD
                );
                let presets_id =
                bevy_remote::RemoteMethodSystemId::Instant(
                    app.main_mut()
                        .world_mut()
                        .register_system(
                            presets::export_presets,
                        ),
                );
                let remote_methods = app
                    .world_mut()
                    .get_resource_mut::<bevy_remote::RemoteMethods>(
                );
                if let Some(mut remote_methods) =
                    remote_methods
                {
                    remote_methods.insert(
                        presets::BRP_SKEIN_PRESETS_METHOD,
                        presets_id,
                    );
                } else {
                    warn!(
                        "bevy_remote::RemoteMethods Resource was not found. Skein can not add custom endpoints without this Resource. `SkeinPlugin::handle_brp` is `{}`, which means `{}` is responsible for adding `bevy_remote::RemotePlugin` and `bevy_remote::http::RemoteHttpPlugin`. {}",
                        self.handle_brp,
                        if self.handle_brp {
                            "skein"
                        } else {
                            "the user"
                        },
                        if self.handle_brp {
                            // if skein was supposed to add the plugins and didn't, then this is likely a skein bug
                            "This is likely a bug: https://github.com/rust-adventure/skein/issues"
                        } else {
                            ""
                        }
                    );
                }
            }
        }
    }
}

/// `SkeinAppExt` extends Bevy's App with the
/// ability to register and insert extra
/// information into Skein's Resources
pub trait SkeinAppExt<V: Reflect> {
    /// Insert a pre-configured Component value
    /// into the Resource that will be used to
    /// serve preset data from the Bevy Remote
    /// Procotol.
    fn insert_skein_preset(
        &mut self,
        preset_name: &str,
        value: V,
    ) -> &mut Self;
}

impl<V: Reflect> SkeinAppExt<V> for App {
    fn insert_skein_preset(
        &mut self,
        #[allow(unused_variables)] preset_name: &str,
        #[allow(unused_variables)] value: V,
    ) -> &mut Self {
        #[cfg(feature = "presets")]
        {
            let mut presets = self
                .main_mut()
                .world_mut()
                .get_resource_or_init::<SkeinPresetRegistry>();

            let component_presets = presets
                .0
                .entry(value.reflect_type_path().to_owned())
                .or_default();

            component_presets
                .entry(preset_name.to_string())
                .and_modify(|_| {
                    warn!(
                        type_path = value.reflect_type_path().to_owned(),
                        ?preset_name,
                        "preset already exists, avoiding overwriting it"
                    );
                })
                .or_insert(Box::new(value));
        }

        self
    }
}

#[derive(Default, Resource)]
struct SkeinPresetRegistry(
    /// TODO: is Box<dyn Reflect> the right bound
    /// here? Could we use something more
    /// restrictive?
    #[allow(dead_code)]
    HashMap<String, HashMap<String, Box<dyn Reflect>>>,
);

#[instrument(skip(
    on_add,
    type_registry,
    gltf_extras,
    gltf_material_extras,
    gltf_mesh_extras,
    gltf_scene_extras,
    names,
    commands,
))]
fn skein_processing(
    on_add: On<
        Add,
        (
            GltfExtras,
            GltfMaterialExtras,
            GltfMeshExtras,
            GltfSceneExtras,
        ),
    >,
    type_registry: Res<AppTypeRegistry>,
    gltf_extras: Query<&GltfExtras>,
    gltf_material_extras: Query<&GltfMaterialExtras>,
    gltf_mesh_extras: Query<&GltfMeshExtras>,
    gltf_scene_extras: Query<&GltfSceneExtras>,
    names: Query<&Name>,
    mut commands: Commands,
) {
    let entity = on_add.entity;

    trace!(
        ?entity,
        name = ?names.get(entity).ok(),
        "skein_processing"
    );

    // Each of the possible extras.
    let gltf_extra =
        gltf_extras.get(entity).map(|v| &v.value);
    let gltf_material_extra =
        gltf_material_extras.get(entity).map(|v| &v.value);
    let gltf_mesh_extra =
        gltf_mesh_extras.get(entity).map(|v| &v.value);
    let gltf_scene_extra =
        gltf_scene_extras.get(entity).map(|v| &v.value);

    for extras in [
        gltf_extra,
        gltf_material_extra,
        gltf_mesh_extra,
        gltf_scene_extra,
    ]
    .iter()
    .filter_map(|p| p.ok())
    {
        trace!(extras);
        let obj = match serde_json::from_str(extras) {
            Ok(Value::Object(obj)) => obj,
            Ok(Value::Null) => {
                if let Ok(name) = names.get(entity) {
                    trace!(
                        "entity {:?} with name {name} had gltf extras which could not be parsed as a serde_json::Value::Object; parsed as Null",
                        entity
                    );
                } else {
                    trace!(
                        "entity {:?} with no Name had gltf extras which could not be parsed as a serde_json::Value::Object; parsed as Null",
                        entity
                    );
                }
                continue;
            }
            Ok(value) => {
                let name = names.get(entity).ok();
                trace!(?entity, ?name, parsed_as=?value, "gltf extras which could not be parsed as a serde_json::Value::Object");
                continue;
            }
            Err(err) => {
                let name = names.get(entity).ok();
                trace!(
                    ?entity,
                    ?name,
                    ?err,
                    "gltf extras which could not be parsed as a serde_json::Value::Object"
                );
                continue;
            }
        };

        let skein = match obj.get("skein") {
            Some(Value::Array(components)) => components,
            Some(value) => {
                let name = names.get(entity).ok();
                error!(?entity, ?name, parsed_as=?value, "the skein gltf extra field could not be parsed as a serde_json::Value::Object");
                continue;
            }
            None => {
                // the skein field not existing is *normal*
                // for most entities
                // a skein field being an object would be an
                // error
                continue;
            }
        };

        // for each component, attempt to reflect it and
        // insert it
        for json_component in skein.iter() {
            let type_registry = type_registry.read();

            // deserialize
            let reflect_deserializer =
                ReflectDeserializer::new(&type_registry);
            let reflect_value = match reflect_deserializer
                .deserialize(json_component)
            {
                Ok(value) => value,
                Err(err) => {
                    error!(
                        ?err,
                        ?obj,
                        "failed to instantiate component data from glTF data"
                    );
                    continue;
                }
            };

            trace!(?reflect_value);
            // TODO: can we do this insert without panic
            // if the intended component
            commands
                .entity(entity)
                .insert_reflect(reflect_value);
        }
    }
}
