//! Skein!
//!
//! Store reflected component data in glTF extras using
//! software like Blender, and insert components based
//! on those extras.
//!
use bevy_app::{App, Plugin};
use bevy_ecs::{
    event::Event,
    hierarchy::Children,
    name::Name,
    observer::Trigger,
    reflect::{AppTypeRegistry, ReflectCommandExt},
    system::{Commands, Query, Res},
};
use bevy_gltf::{
    GltfExtras, GltfMaterialExtras, GltfMeshExtras,
    GltfSceneExtras,
};
use bevy_log::{error, trace};
use bevy_reflect::{serde::ReflectDeserializer, Reflect};
use bevy_scene::SceneInstanceReady;
use serde::de::DeserializeSeed;
use serde_json::Value;
use tracing::instrument;

/// [`SkeinPlugin`] is the main plugin.
///
/// This will add Scene postprocessing which will introspect
/// glTF extras and set up the expected components using
/// Bevy's reflection infrastructure.
pub struct SkeinPlugin {
    /// Whether Skein should handle adding the Bevy Remote Protocol
    /// plugins.
    ///
    /// use `false` if you want to handle setting up BRP yourself
    handle_brp: bool,
}

impl Default for SkeinPlugin {
    fn default() -> Self {
        Self { handle_brp: true }
    }
}

impl Plugin for SkeinPlugin {
    fn build(&self, app: &mut App) {
        app.add_observer(postprocess_scene);

        if self.handle_brp {
            app.add_plugins((
                bevy_remote::RemotePlugin::default(),
                bevy_remote::http::RemoteHttpPlugin::default(),
            ));
        }
    }
}

#[instrument(skip(
    trigger,
    type_registry,
    children,
    gltf_extras,
    gltf_material_extras,
    gltf_mesh_extras,
    gltf_scene_extras,
    names,
    commands,
))]
fn postprocess_scene(
    trigger: Trigger<SceneInstanceReady>,
    type_registry: Res<AppTypeRegistry>,
    children: Query<&Children>,
    gltf_extras: Query<&GltfExtras>,
    gltf_material_extras: Query<&GltfMaterialExtras>,
    gltf_mesh_extras: Query<&GltfMeshExtras>,
    gltf_scene_extras: Query<&GltfSceneExtras>,
    names: Query<&Name>,
    mut commands: Commands,
) {
    trace!("global_scene_instance_ready");
    for entity in
        children.iter_descendants(trigger.target())
    {
        let Ok(extras) = gltf_extras
            .get(entity)
            .map(|v| &v.value)
            .or(gltf_material_extras
                .get(entity)
                .map(|v| &v.value))
            .or(gltf_mesh_extras
                .get(entity)
                .map(|v| &v.value))
            .or(gltf_scene_extras
                .get(entity)
                .map(|v| &v.value))
        else {
            continue;
        };

        let obj = match serde_json::from_str(extras) {
            Ok(Value::Object(obj)) => obj,
            Ok(Value::Null) => {
                if let Ok(name) = names.get(entity) {
                    trace!("entity {:?} with name {name} had gltf extras which could not be parsed as a serde_json::Value::Object; parsed as Null", entity);
                } else {
                    trace!("entity {:?} with no Name had gltf extras which could not be parsed as a serde_json::Value::Object; parsed as Null", entity);
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
                trace!(?entity, ?name, ?err, "gltf extras which could not be parsed as a serde_json::Value::Object");
                continue;
            }
        };

        let skein = match obj.get("skein") {
            Some(Value::Object(components)) => components,
            Some(value) => {
                let name = names.get(entity).ok();
                error!(?entity, ?name, parsed_as=?value, "the skein gltf extra field could not be parsed as a serde_json::Value::Object");
                continue;
            }
            None => {
                // the skein field not existing is *normal* for most
                // entities
                // a skein field being an array would be an error
                continue;
            }
        };

        // construct a Value::Object for each component entry because Bevy's reflection expects an
        // Value::Object with a single-key where the key is the component path and the value is the
        // component value
        for (key, value) in skein.iter() {
            let mut json_component_inner =
                serde_json::Map::new();
            json_component_inner
                .insert(key.clone(), value.clone());
            let json_component =
                Value::Object(json_component_inner);

            let type_registry = type_registry.read();

            // deserialize
            let reflect_deserializer =
                ReflectDeserializer::new(&type_registry);
            let reflect_value = reflect_deserializer
                .deserialize(json_component)
                .unwrap();

            // TODO: can we do this insert without panic
            // if the intended component
            commands
                .entity(entity)
                .insert_reflect(reflect_value);
        }
    }

    // trigger the event again so that consumers can have a
    // "real" SceneInstanceReady event to consume if they
    // want to
    //
    // 1. spawn
    // 2. let skein postprocess
    // 3. then handle the resulting scene
    commands.trigger_targets(
        SkeinSceneInstanceReady(*trigger.event()),
        trigger.target(),
    );
}

/// A duplicate of the original [`SceneInstanceReady`] event
/// that fires after skein has post-processed the scene.
///
/// Use an observer targeting this event if you want to use
/// [`SceneInstanceReady`] but you also want components from
/// your gltf file to be applied first.
///
/// ```rust
/// use bevy::prelude::*;
/// use skein::SkeinSceneInstanceReady;
/// use serde::{Serialize, Deserialize};
///
/// #[derive(
///   Component, Reflect, Serialize, Deserialize, Debug,
/// )]
/// #[reflect(Component, Serialize, Deserialize)]
/// struct Character {
///     name: String,
/// }
///
/// fn check_insertions(
///     trigger: Trigger<SkeinSceneInstanceReady>,
///     children: Query<&Children>,
///     levels: Query<&Character>,
/// ) {
///     for entity in
///         children.iter_descendants(trigger.target())
///     {
///         let Ok(level) = levels.get(entity) else {
///             continue;
///         };
///         info!(?level);
///     }
///     }
/// ```
#[derive(Debug, Event, Reflect)]
pub struct SkeinSceneInstanceReady(pub SceneInstanceReady);

#[cfg(test)]
mod tests {
    use super::*;
    use bevy::prelude::*;
    use bevy_reflect::{
        serde::ReflectSerializer, TypeRegistry,
    };
    use serde::{Deserialize, Serialize};

    #[derive(
        Component, Reflect, Serialize, Deserialize, Debug,
    )]
    #[reflect(Component, Serialize, Deserialize)]
    struct Player {
        name: String,
        power: f32,
        test: i32,
    }

    #[test]
    fn struct_fields() {
        let value = Player {
            name: "Chris Biscardi".to_string(),
            power: 100.,
            test: 4,
        };

        let type_registry = TypeRegistry::new();

        // serialize
        let serializer =
            ReflectSerializer::new(&value, &type_registry);
        let json_string =
            serde_json::ser::to_string(&serializer)
                .unwrap();

        assert_eq!(
            json_string,
            r#"{"skein::tests::Player":{"name":"Chris Biscardi","power":100.0,"test":4}}"#
        );
    }

    #[derive(
        Component, Reflect, Serialize, Deserialize, Debug,
    )]
    #[reflect(Component, Serialize, Deserialize)]
    struct TeamMember {
        player: Player,
        team: Team,
    }

    #[derive(Reflect, Serialize, Deserialize, Debug)]
    enum Team {
        Green,
        Red,
        Blue,
    }

    #[test]
    fn deep_struct_fields() {
        let value = TeamMember {
            player: Player {
                name: "Chris Biscardi".to_string(),
                power: 100.,
                test: 4,
            },
            team: Team::Green,
        };

        let type_registry = TypeRegistry::new();

        // serialize
        let serializer =
            ReflectSerializer::new(&value, &type_registry);
        let json_string =
            serde_json::ser::to_string(&serializer)
                .unwrap();

        assert_eq!(
            json_string,
            r#"{"skein::tests::TeamMember":{"player":{"name":"Chris Biscardi","power":100.0,"test":4},"team":"Green"}}"#
        );
    }

    #[derive(
        Component, Reflect, Serialize, Deserialize, Debug,
    )]
    #[reflect(Component, Serialize, Deserialize)]
    struct TupleStruct(u32);

    #[test]
    fn tuple_struct() {
        let value = TupleStruct(12);

        let type_registry = TypeRegistry::new();

        // serialize
        let serializer =
            ReflectSerializer::new(&value, &type_registry);
        let json_string =
            serde_json::ser::to_string(&serializer)
                .unwrap();

        assert_eq!(
            json_string,
            r#"{"skein::tests::TupleStruct":12}"#
        );
    }

    #[derive(
        Component, Reflect, Serialize, Deserialize, Debug,
    )]
    #[reflect(Component, Serialize, Deserialize)]
    struct Marker;

    #[test]
    fn marker_component() {
        let value = Marker;

        let type_registry = TypeRegistry::new();

        // serialize
        let serializer =
            ReflectSerializer::new(&value, &type_registry);
        let json_string =
            serde_json::ser::to_string(&serializer)
                .unwrap();

        assert_eq!(
            json_string,
            r#"{"skein::tests::Marker":{}}"#
        );
    }

    #[derive(
        Component, Reflect, Serialize, Deserialize, Debug,
    )]
    #[reflect(Component, Serialize, Deserialize)]
    enum TaskPriority {
        High,
        Medium,
        Low,
    }

    #[test]
    fn enum_component() {
        let value = TaskPriority::High;

        let type_registry = TypeRegistry::new();

        // serialize
        let serializer =
            ReflectSerializer::new(&value, &type_registry);
        let json_string =
            serde_json::ser::to_string(&serializer)
                .unwrap();

        assert_eq!(
            json_string,
            r#"{"skein::tests::TaskPriority":"High"}"#
        );
    }

    #[derive(
        Component, Reflect, Serialize, Deserialize, Debug,
    )]
    #[reflect(Component, Serialize, Deserialize)]
    enum SomeThings {
        OneThing { name: String },
        Low(i32),
    }

    #[test]
    fn enum_component_with_fields() {
        let value = SomeThings::OneThing {
            name: "testing".to_string(),
        };

        let type_registry = TypeRegistry::new();

        // serialize
        let serializer =
            ReflectSerializer::new(&value, &type_registry);
        let json_string =
            serde_json::ser::to_string(&serializer)
                .unwrap();

        assert_eq!(
            json_string,
            r#"{"skein::tests::SomeThings":{"OneThing":{"name":"testing"}}}"#
        );
    }
}
