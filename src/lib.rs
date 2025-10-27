#![doc = include_str!("../README.md")]
use std::net::IpAddr;

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
use bevy_log::{error, trace};
use bevy_platform::collections::HashMap;
use bevy_reflect::{Reflect, serde::ReflectDeserializer};
use bevy_remote::http::{DEFAULT_ADDR, DEFAULT_PORT};
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
#[cfg(feature = "presets")]
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
    /// Host address for the bevy protocol.
    pub address: IpAddr,
    /// Port for the bevy protocol.
    pub port: u16,
}

impl Default for SkeinPlugin {
    fn default() -> Self {
        let dev = cfg!(debug_assertions);
        Self {
            handle_brp: dev,
            address: DEFAULT_ADDR,
            port: DEFAULT_PORT,
        }
    }
}

impl SkeinPlugin {
    /// Builder function to use bevy protocol
    /// with custom host address.
    pub fn with_address(
        &mut self,
        address: IpAddr,
    ) -> &mut Self {
        self.address = address;
        self
    }

    /// Builder function to use bevy protocol
    /// with custom port.
    pub fn with_port(&mut self, port: u16) -> &mut Self {
        self.port = port;
        self
    }
}

impl Plugin for SkeinPlugin {
    fn build(&self, app: &mut App) {
        app.init_resource::<SkeinPresetRegistry>()
            .add_observer(skein_processing);

        #[cfg(all(
            not(target_family = "wasm"),
            feature = "brp"
        ))]
        if self.handle_brp {
            #[allow(unused_mut)]
            let mut remote_plugin =
                bevy_remote::RemotePlugin::default();

            #[cfg(feature = "presets")]
            {
                remote_plugin = remote_plugin.with_method(
                    presets::BRP_SKEIN_PRESETS_METHOD,
                    presets::export_presets,
                );
            }

            app.add_plugins((
                remote_plugin,
                bevy_remote::http::RemoteHttpPlugin::default().with_address(self.address).with_port(self.port)
            ));
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
