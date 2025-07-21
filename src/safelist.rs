use bevy_ecs::{
    reflect::AppTypeRegistry, system::In, world::World,
};
use bevy_platform::collections::{HashMap, HashSet};
use bevy_reflect::{TypeInfo, VariantInfo};
use bevy_remote::{
    BrpError, BrpResult, error_codes,
    schemas::json_schema::JsonSchemaBevyType,
};
use serde::{Deserialize, Serialize};
use serde_json::Value;

/// The method path for a `bevy/registry/schema` request.
pub const BRP_REGISTRY_SCHEMA_METHOD: &str =
    "skein/registry/schema";

/// Constraints that can be placed on a query to include or exclude
/// certain definitions.
#[derive(
    Debug, Serialize, Deserialize, Clone, Default, PartialEq,
)]
pub struct BrpJsonSchemaQueryFilter {
    /// The crate name of the type name of each component that must not be
    /// present on the entity for it to be included in the results.
    #[serde(
        skip_serializing_if = "Vec::is_empty",
        default
    )]
    pub safelist_types: Vec<String>,

    /// The crate name of the type name of each component that must be present
    /// on the entity for it to be included in the results.
    #[serde(
        skip_serializing_if = "Vec::is_empty",
        default
    )]
    pub safelist_crates: Vec<String>,
}

/// Handles a `bevy/registry/schema` request (list all registry types in form of schema) coming from a client.
pub fn export_registry_types(
    In(params): In<Option<Value>>,
    world: &World,
) -> BrpResult {
    let filter: BrpJsonSchemaQueryFilter = match params {
        None => Default::default(),
        Some(params) => parse(params)?,
    };

    let types = world.resource::<AppTypeRegistry>();
    let types = types.read();
    let mut deps = HashSet::new();
    let schemas = types
        .iter()
        .map(|type_registration| (bevy_remote::schemas::json_schema::export_type(&type_registration), type_registration.type_info()))
        .filter(|((_, schema), _)| {
            if !filter.safelist_crates.is_empty() {
                return schema
                    .crate_name
                    .as_ref()
                    .is_some_and(|crate_name| {
                        filter
                            .safelist_crates
                            .contains(&crate_name)
                    });
            } else {
                return true;
            }
        })
        .inspect(|((_, _), type_info)| {
            for dep in get_type_dependencies(&type_info) {
                deps.insert(dep);
            }
        })
        .map(|(v,_)| v)
        .collect::<HashMap<String, JsonSchemaBevyType>>();

    dbg!(deps);
    dbg!(schemas.get("test_components::TeamMember"));

    serde_json::to_value(schemas)
        .map_err(BrpError::internal)
}

/// A helper function used to parse a `serde_json::Value`.
fn parse<T: for<'de> Deserialize<'de>>(
    value: Value,
) -> Result<T, BrpError> {
    serde_json::from_value(value).map_err(|err| BrpError {
        code: error_codes::INVALID_PARAMS,
        message: err.to_string(),
        data: None,
    })
}

fn get_type_dependencies(
    type_info: &TypeInfo,
) -> Vec<&str> {
    match type_info {
        TypeInfo::Struct(info) => {
            return info
                .iter()
                .flat_map(|field| match field.type_info() {
                    Some(next_type_info) => {
                        get_type_dependencies(
                            &next_type_info,
                        )
                    }
                    None => vec![],
                })
                .collect::<Vec<_>>();
        }

        TypeInfo::Enum(info) => {
            let simple = info.iter().all(|variant| {
                matches!(variant, VariantInfo::Unit(_))
            });
            if simple {
                return vec![info.type_path()];
            } else {
                return info
                    .iter()
                    .flat_map(|variant| match variant {
                        VariantInfo::Struct(v) => {
                            return v
                .iter()
                .flat_map(|field| match field.type_info() {
                    Some(next_type_info) => {
                        get_type_dependencies(
                            &next_type_info,
                        )
                    }
                    None => vec![],
                })
                .collect::<Vec<_>>();
                        }
                        VariantInfo::Tuple(v) => return v
                            .iter()
                            .flat_map(|field| {
                                match field.type_info() {
                                Some(next_type_info) => {
                                    get_type_dependencies(
                                        &next_type_info,
                                    )
                                }
                                None => vec![],
                            }
                            })
                            .collect::<Vec<_>>(),
                        VariantInfo::Unit(_) => vec![],
                    })
                    .collect::<Vec<_>>();
            }
        }
        TypeInfo::TupleStruct(info) => {
            return info
                .iter()
                .flat_map(|field| match field.type_info() {
                    Some(next_type_info) => {
                        get_type_dependencies(
                            &next_type_info,
                        )
                    }
                    None => vec![],
                })
                .collect::<Vec<_>>();
        }
        TypeInfo::List(info) => match info.item_info() {
            Some(type_info) => vec![type_info.type_path()],
            None => vec![],
        },
        TypeInfo::Array(info) => match info.item_info() {
            Some(type_info) => vec![type_info.type_path()],
            None => vec![],
        },
        TypeInfo::Map(_info) => {
            // info.key_type
            // info.value_type
            return vec![];
        }
        TypeInfo::Tuple(info) => info
            .iter()
            .flat_map(|field| match field.type_info() {
                Some(next_type_info) => {
                    get_type_dependencies(&next_type_info)
                }
                None => vec![],
            })
            .collect::<Vec<_>>(),
        TypeInfo::Set(info) => vec![info.value_ty().path()],
        TypeInfo::Opaque(info) => {
            vec![info.type_path()]
        }
    }
}
