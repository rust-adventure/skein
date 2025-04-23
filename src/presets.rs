use core::any::TypeId;

use bevy_ecs::{
    reflect::{AppTypeRegistry, ReflectComponent},
    system::In,
    world::World,
};
use bevy_platform::collections::HashMap;
use bevy_reflect::{
    Reflect, TypeRegistration, prelude::ReflectDefault,
    serde::ReflectSerializer,
};
use serde_json::Value;

use bevy_remote::{BrpError, BrpResult};
use tracing::trace;

use crate::SkeinPresetRegistry;

/// The method path for a `skein/presets` request.
pub const BRP_SKEIN_PRESETS_METHOD: &str = "skein/presets";

/// Handles a `skein/presets` request coming from a client.
pub fn export_presets(
    In(_): In<Option<Value>>,
    world: &World,
) -> BrpResult {
    let types = world.resource::<AppTypeRegistry>().read();

    let presets =
        world.resource::<SkeinPresetRegistry>();

   let mut all_serialized_presets = presets.0.iter().map(|(type_path, component_presets)| {
        let serialized_presets = component_presets.iter().filter_map(|(preset_name, reflected)| {
            let reflect_serializer = ReflectSerializer::new(
                reflected.as_reflect(),
                &types,
            );
            // the serialized reflection form of the values here is
            // {
            //   "some_module::MyComponent": { my_int: 3 }
            // }
            // 
            // So we want to 
            let Ok(serde_json::Value::Object(output)) =
                serde_json::to_value(&reflect_serializer)
            else {
                trace!(?preset_name, ?reflected, "unable to serialize for presets endpoint");
    
                return None;
            };
            Some((preset_name.to_string(), output[type_path].clone()))
        })
        .collect::<HashMap<String, Value>>();
        (type_path.clone(), serialized_presets)
    }).collect::<HashMap<String, HashMap<String, Value>>>();


    for (type_path, default_value) in types
        .iter()
        .filter_map(export_default_preset)
        .filter_map(|(type_path, reflected)| {
            let reflect_serializer = ReflectSerializer::new(
                reflected.as_reflect(),
                &types,
            );
            let Ok(serde_json::Value::Object(output)) =
                serde_json::to_value(&reflect_serializer)
            else {
                trace!(?type_path, ?reflected, "unable to serialize for presets endpoint");

                return None;
            };
            Some((type_path, output[type_path].clone()))
        }) {
            all_serialized_presets.entry(type_path.to_string()).and_modify(|map| {
                map.insert("default".to_string(), default_value.clone());
            }).or_insert(
                HashMap::from([("default".to_string(), default_value)])
            );
        }

    serde_json::to_value(all_serialized_presets)
        .map_err(BrpError::internal)
}

/// Constructs the Default value for a given type
fn export_default_preset(
    reg: &TypeRegistration,
) -> Option<(&str, Box<dyn Reflect>)> {
    let t = reg.type_info();
    let binding = t.type_path_table();

    let type_path = binding.path();

    // we're only interested in Components that implement Default,
    // so we test for ReflectComponent and ReflectDefault and return
    // None to filter this value out
    if !(reg
        .data_by_id(TypeId::of::<ReflectComponent>())
        .is_some()
        && reg
            .data_by_id(TypeId::of::<ReflectDefault>())
            .is_some())
    {
        return None;
    }

    let reflect_default = reg.data::<ReflectDefault>()?;
    let value = reflect_default.default();

    Some((type_path, value))
}
