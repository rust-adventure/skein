#![doc = include_str!("../README.md")]
use bevy_app::{App, Plugin, Startup};
use bevy_ecs::{
    name::Name,
    observer::Trigger,
    reflect::{AppTypeRegistry, ReflectCommandExt},
    resource::Resource,
    system::{Commands, Query, Res},
    world::OnAdd,
};
use bevy_gltf::{
    GltfExtras, GltfMaterialExtras, GltfMeshExtras,
    GltfSceneExtras,
};
use bevy_log::{error, trace};
use bevy_platform::collections::HashMap;
use bevy_reflect::{Reflect, serde::ReflectDeserializer};
use serde::{Deserialize, Serialize, de::DeserializeSeed};
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

/// Safelists are used for providing a well-defined
/// Component API to artists using Blender. By
/// enabling this feature, you can limit the available
/// components Blender users will see.
///
/// Doing this in combination with putting all Blender
/// Components in one (or a few) crates, allows users
/// to have a high degree of control over the Blender
/// user experience.
#[cfg(feature = "safelist")]
pub mod safelist;

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
    /// use `false` if you want to handle setting
    /// up BRP yourself
    #[allow(dead_code)]
    pub handle_brp: bool,
    /// When the `write_manifest_and_exit` feature is enabled,
    /// This value controls whether the currently running
    /// application should actually write the skein
    /// manifest file and exit.
    ///
    /// By default this value is true. Which means when the
    /// `write_manifest_and_exit` feature is enabled, the program
    /// will write the file and exit by default.
    ///
    /// If you want to be able to write the manifest from a
    /// previously compiled build, such as when distributing a
    /// test game binary, set this value to `false` and choose
    /// your own adventure for how to configure it when you want
    /// to. (one potential option is to do your own CLI argument
    /// parsing)
    pub write_manifest_and_exit: bool,
}

impl Default for SkeinPlugin {
    fn default() -> Self {
        Self {
            handle_brp: true,
            // default is true, because the feature is off by default,
            // so turning the feature on should cause this to execute.
            //
            // use false if you want to be able to toggle this in a dev
            // build that is being distributed as a binary.
            write_manifest_and_exit: true,
        }
    }
}

impl Plugin for SkeinPlugin {
    fn build(&self, app: &mut App) {
        app.init_resource::<SkeinPresetRegistry>()
            .add_observer(skein_processing);

        #[cfg(feature = "write_manifest_and_exit")]
        app.add_systems(Startup, write_manifest_and_exit);

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

            remote_plugin = remote_plugin.with_method(
                safelist::BRP_REGISTRY_SCHEMA_METHOD,
                safelist::export_registry_types,
            );

            app.add_plugins((
                remote_plugin,
                bevy_remote::http::RemoteHttpPlugin::default(),
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
    trigger,
    type_registry,
    gltf_extras,
    gltf_material_extras,
    gltf_mesh_extras,
    gltf_scene_extras,
    names,
    commands,
))]
fn skein_processing(
    trigger: Trigger<
        OnAdd,
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
    let entity = trigger.target();

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

/// The format written to disk when using an "offline" registry
#[derive(Serialize, Deserialize)]
struct SkeinManifest {
    /// manifest version. Only bumped if there's a breaking change in the data that we need to communicate to blender
    version: usize,
    /// the safelisted crates whose components will be shown in Blender; empty Vec is no filter.
    crate_safelist: Vec<String>,
    /// what version of bevy_skein was used to create this data?
    created_using_bevy_skein_version: &'static str,
    /// available presets/default values for components
    presets: Option<serde_json::Value>,
    /// type_reflection data
    registry: serde_json::Value,
}

impl Default for SkeinManifest {
    fn default() -> Self {
        Self {
            version: 1,
            crate_safelist: Default::default(),
            created_using_bevy_skein_version: env!(
                "CARGO_PKG_VERSION"
            ),
            presets: Default::default(),
            registry: Default::default(),
        }
    }
}

#[cfg(feature = "write_manifest_and_exit")]
fn write_manifest_and_exit(
    mut world: &mut bevy_ecs::world::World,
) -> bevy_ecs::error::Result {
    use crate::safelist::export_registry_types;
    use bevy_app::AppExit;
    use bevy_ecs::{
        event::EventWriter, system::SystemState,
    };
    let types_schema = world
        .run_system_cached_with(
            export_registry_types,
            None,
        )?
        .map_err(|brp_error| format!("{:?}", brp_error))?;
    let registry_save_path = std::path::Path::new(
        "skein.manifest.registry.json",
    );

    let manifest = SkeinManifest {
        crate_safelist: vec![],
        presets: None,
        registry: types_schema,
        ..Default::default()
    };

    let writer = std::fs::File::create(registry_save_path)?;
    serde_json::to_writer_pretty(writer, &manifest)?;

    let mut system_state: SystemState<
        EventWriter<AppExit>,
    > = SystemState::new(&mut world);

    let mut exit_event = system_state.get_mut(&mut world);

    exit_event.write(AppExit::Success);
    Ok(())
}
