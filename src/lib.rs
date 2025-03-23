#![doc = include_str!("../README.md")]
use bevy_app::{App, Plugin};
use bevy_ecs::{
    name::Name,
    observer::Trigger,
    reflect::{AppTypeRegistry, ReflectCommandExt},
    system::{Commands, Query, Res},
    world::OnAdd,
};
use bevy_gltf::{
    GltfExtras, GltfMaterialExtras, GltfMeshExtras,
    GltfSceneExtras,
};
use bevy_log::{error, trace};
use bevy_reflect::serde::ReflectDeserializer;
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
        app.add_observer(skein_processing);

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
                // the skein field not existing is *normal* for most
                // entities
                // a skein field being an object would be an error
                continue;
            }
        };

        // for each component, attempt to reflect it and insert it
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

#[cfg(test)]
mod tests {
    use std::str::FromStr;

    use bevy::{asset::uuid::Uuid, prelude::*};
    use bevy_reflect::{
        TypeRegistry, serde::ReflectSerializer,
    };
    use test_components::*;

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
            r#"{"test_components::Player":{"name":"Chris Biscardi","power":100.0,"test":4}}"#
        );
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
            r#"{"test_components::TeamMember":{"player":{"name":"Chris Biscardi","power":100.0,"test":4},"team":"Green"}}"#
        );
    }

    #[test]
    fn tuple_struct() {
        let value = ATupleStruct(12);

        let type_registry = TypeRegistry::new();

        // serialize
        let serializer =
            ReflectSerializer::new(&value, &type_registry);
        let json_string =
            serde_json::ser::to_string(&serializer)
                .unwrap();

        assert_eq!(
            json_string,
            r#"{"test_components::ATupleStruct":12}"#
        );
    }

    #[test]
    fn multi_element_tuple_struct() {
        let value = MultiElementTupleStruct(
            12,
            Vec3::ZERO,
            2,
            "testing".to_string(),
        );

        let type_registry = TypeRegistry::new();

        // serialize
        let serializer =
            ReflectSerializer::new(&value, &type_registry);
        let json_string =
            serde_json::ser::to_string(&serializer)
                .unwrap();

        assert_eq!(
            json_string,
            r#"{"test_components::MultiElementTupleStruct":[12,{"x":0.0,"y":0.0,"z":0.0},2,"testing"]}"#
        );
    }

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
            r#"{"test_components::Marker":{}}"#
        );
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
            r#"{"test_components::TaskPriority":"High"}"#
        );
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
            r#"{"test_components::SomeThings":{"OneThing":{"name":"testing"}}}"#
        );
    }

    #[test]
    fn enum_component_with_fields_alt() {
        let value = SomeThings::Low(12);

        let type_registry = TypeRegistry::new();

        // serialize
        let serializer =
            ReflectSerializer::new(&value, &type_registry);
        let json_string =
            serde_json::ser::to_string(&serializer)
                .unwrap();

        assert_eq!(
            json_string,
            r#"{"test_components::SomeThings":{"Low":12}}"#
        );
    }

    #[test]
    fn an_optional_name() {
        let value = AnOptionalName {
            name: Some("A Test Name".to_string()),
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
            r#"{"test_components::AnOptionalName":{"name":"A Test Name"}}"#
        );

        let value = AnOptionalName { name: None };
        // serialize
        let serializer =
            ReflectSerializer::new(&value, &type_registry);
        let json_string =
            serde_json::ser::to_string(&serializer)
                .unwrap();

        assert_eq!(
            json_string,
            r#"{"test_components::AnOptionalName":{"name":null}}"#
        );
    }

    #[test]
    fn non_zero_numbers() {
        let value = NonZeroNumbers {
            small: std::num::NonZeroU8::new(255).unwrap(),
            an_int: std::num::NonZeroI16::new(-493)
                .unwrap(),
        };

        let mut type_registry = TypeRegistry::new();
        type_registry.register::<NonZeroNumbers>();

        // serialize
        let serializer =
            ReflectSerializer::new(&value, &type_registry);
        let json_string =
            serde_json::ser::to_string(&serializer)
                .unwrap();

        assert_eq!(
            json_string,
            r#"{"test_components::NonZeroNumbers":{"small":255,"an_int":-493}}"#
        );
    }

    #[test]
    fn bucket_of_types() {
        let value = BucketOfTypes {
            entity: Entity::PLACEHOLDER,
            // force a uuid value for testing purposes
            uuid: Uuid::from_str(
                "16c27292-862e-4555-af16-d3d8e624c6de",
            )
            .unwrap(),
            bvec: BVec3A::new(true, false, true),
        };

        let mut type_registry = TypeRegistry::new();
        type_registry.register::<BucketOfTypes>();

        // serialize
        let serializer =
            ReflectSerializer::new(&value, &type_registry);
        let json_string =
            serde_json::ser::to_string(&serializer)
                .unwrap();

        assert_eq!(
            json_string,
            r#"{"test_components::BucketOfTypes":{"entity":8589934591,"uuid":"16c27292-862e-4555-af16-d3d8e624c6de","bvec":[true,false,true]}}"#
        );
    }

    #[test]
    fn enum_component_rich_and_unit_enum() {
        let value = RichAndUnitEnum::Player(Player {
            name: "Chris".to_string(),
            power: 10.,
            test: 42,
        });

        let type_registry = TypeRegistry::new();

        // serialize
        let serializer =
            ReflectSerializer::new(&value, &type_registry);
        let json_string =
            serde_json::ser::to_string(&serializer)
                .unwrap();

        assert_eq!(
            json_string,
            r#"{"test_components::RichAndUnitEnum":{"Player":{"name":"Chris","power":10.0,"test":42}}}"#
        );
    }

    #[test]
    fn enum_component_rich_and_unit_enum_alt() {
        let value = RichAndUnitEnum::NotAPlayer;

        let type_registry = TypeRegistry::new();

        // serialize
        let serializer =
            ReflectSerializer::new(&value, &type_registry);
        let json_string =
            serde_json::ser::to_string(&serializer)
                .unwrap();

        assert_eq!(
            json_string,
            r#"{"test_components::RichAndUnitEnum":"NotAPlayer"}"#
        );
    }

    #[test]
    fn a_struct_with_color() {
        let value = AStructWithColor {
            base: Color::hsl(20., 50., 50.),
            highlight: Color::oklch(1., 1., 1.),
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
            r#"{"test_components::AStructWithColor":{"base":{"Hsla":{"hue":20.0,"saturation":50.0,"lightness":50.0,"alpha":1.0}},"highlight":{"Oklcha":{"lightness":1.0,"chroma":1.0,"hue":1.0,"alpha":1.0}}}}"#
        );
    }

    #[test]
    fn timer_support() {
        let value = TimerContainer(Timer::from_seconds(
            2.,
            TimerMode::Once,
        ));

        let mut type_registry = TypeRegistry::new();

        type_registry.register::<TimerContainer>();

        // serialize
        let serializer =
            ReflectSerializer::new(&value, &type_registry);
        let json_string =
            serde_json::ser::to_string(&serializer)
                .unwrap();

        assert_eq!(
            json_string,
            r#"{"test_components::TimerContainer":{"stopwatch":{"elapsed":{"secs":0,"nanos":0},"is_paused":false},"duration":{"secs":2,"nanos":0},"mode":"Once","finished":false,"times_finished_this_tick":0}}"#
        );
    }

    #[test]
    fn vec3_support() {
        let value = LinearVelocity(Vec3::splat(2.));

        let mut type_registry = TypeRegistry::new();

        type_registry.register::<TimerContainer>();

        // serialize
        let serializer =
            ReflectSerializer::new(&value, &type_registry);
        let json_string =
            serde_json::ser::to_string(&serializer)
                .unwrap();

        assert_eq!(
            json_string,
            r#"{"test_components::LinearVelocity":{"x":2.0,"y":2.0,"z":2.0}}"#
        );
    }
}
