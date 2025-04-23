use bevy::{math::*, prelude::*};
use std::num::{NonZeroI16, NonZeroU8};

/// A Component with fields
#[derive(Component, Reflect, Debug)]
#[reflect(Component)]
pub struct ThisIsOverThePythonKeyLengthLimitForBlenderProperties
{
    pub are_you_feeling_it_now_mr_krabs: bool,
    pub im_ready_im_ready_im_ready: String,
}

/// A Component with fields
#[derive(Component, Reflect, Debug)]
#[reflect(Component, Default)]
pub struct Player {
    pub name: String,
    pub power: f32,
    pub test: i32,
}

impl Default for Player {
    fn default() -> Self {
        Self {
            name: "Chris".to_string(),
            power: 85.23,
            test: 20,
        }
    }
}

/// A Component that includes other "non-scalar"
/// types in the values
#[derive(Component, Reflect, Debug, Default)]
#[reflect(Component, Default)]
pub struct TeamMember {
    pub player: Player,
    pub team: Team,
}

#[derive(Reflect, Debug, Default)]
#[reflect(Default)]
pub enum Team {
    Green,
    #[default]
    Red,
    Blue,
}

/// Single-element tuple structs turn into
/// just the inner value
#[derive(Component, Reflect, Debug)]
#[reflect(Component)]
pub struct ATupleStruct(pub u32);

/// MultiElementTupleStruct is not currently
/// supported in the Blender addon. if you have a
/// use case for this that isn't solvable by
/// converting to a named field struct, open an
/// issue or a PR
#[derive(Component, Reflect, Debug)]
#[reflect(Component)]
pub struct MultiElementTupleStruct(
    pub u32,
    pub Vec3,
    pub i32,
    pub String,
);

/// Marker components turn into empty object
/// values
#[derive(Component, Reflect, Debug)]
#[reflect(Component)]
pub struct Marker;

/// An all-unit-struct enum, which
/// turns into a string like `"High"`
#[derive(Component, Reflect, Debug)]
#[reflect(Component)]
pub enum TaskPriority {
    High,
    Medium,
    Low,
}

/// a "rich" enum with a struct variant and
/// a tuple struct variant
#[derive(Component, Reflect, Debug)]
#[reflect(Component, Default)]
pub enum SomeThings {
    OneThing { name: String },
    Low(i32),
}

impl Default for SomeThings {
    fn default() -> Self {
        SomeThings::Low(2)
    }
}

/// No support for `Timer` yet
#[derive(Component, Reflect, Debug)]
#[reflect(Component)]
pub struct TimerContainer(pub Timer);

/// A Component that uses an Option,
/// which is handled specially. `Some(value)`
/// results in just the `value` and `None`
/// results in `null`
#[derive(Component, Reflect, Debug)]
#[reflect(Component, Default)]
pub struct AnOptionalName {
    pub name: Option<String>,
}

impl Default for AnOptionalName {
    fn default() -> Self {
        Self {
            name: Some("Chris".to_string()),
        }
    }
}

/// A type containing a few NonZero types.
/// NonZero types are basically regular numbers
/// with "no 0 value", so we don't need to test
/// all NonZero types
#[derive(Component, Reflect, Debug)]
#[reflect(Component)]
pub struct NonZeroNumbers {
    pub small: NonZeroU8,
    pub an_int: NonZeroI16,
}

/// A selection of values that are string-ish
#[derive(Component, Reflect, Debug)]
#[reflect(Component)]
pub struct BucketOfTypes {
    /// Notably Entities can be represented by
    /// integers, but that doesn't necessarily
    /// relate to the entities in a
    /// running Bevy application
    pub entity: Entity,
    /// uuids are mostly used in Assets, which we
    /// don't really deal with inside Blender
    pub uuid: bevy::asset::uuid::Uuid,
    /// edge case-ish, but should be supportable
    /// alongside arrays
    pub bvec: BVec3A,
}

/// An enum that has a rich struct variant
/// and a unit variant
#[derive(Component, Reflect, Debug)]
#[reflect(Component, Default)]
pub enum RichAndUnitEnum {
    Player(Player),
    NotAPlayer,
}

impl Default for RichAndUnitEnum {
    fn default() -> Self {
        RichAndUnitEnum::NotAPlayer
    }
}

/// People use Color quite a bit,
/// here's a struct that uses it
#[derive(Component, Reflect, Debug)]
#[reflect(Component)]
pub struct AStructWithColor {
    pub base: Color,
    pub highlight: Color,
    // TODO: what about LinearRgba?
}

/// Avian has LinearVelocity/AngularVelocity
/// that is basically a Vec3
#[derive(Component, Reflect, Debug)]
#[reflect(Component)]
pub struct LinearVelocity(pub Vec3);

#[derive(Debug, Component, Reflect)]
#[reflect(Component)]
pub enum PlatformBehavior {
    Rotate90X,
    Rotate90Y,
    MoveLinear { start: Vec3, end: Vec3 },
}

#[derive(Component, Reflect)]
#[reflect(Component)]
pub struct SuperGlam {
    // vec2: Vec2,
    // vec3: Vec3,
    // vec4: Vec4,
    // quat: Quat, // xyzw
    // mat2: Mat2, // 4 value
    // mat3: Mat3, // 9 values
    // mat4: Mat4, // 16 values
    // affine2: bevy::math::Affine2,
    // x_axis.x
    // x_axis.y
    // y_axis.x
    // y_axis.y
    // z_axis.x
    // z_axis.y
    // affine3: bevy::math::Affine3,
    // x_axis.x
    // x_axis.y
    // x_axis.z
    // y_axis.x
    // y_axis.y
    // y_axis.z
    // z_axis.x
    // z_axis.y
    // z_axis.z
    // w_axis.x
    // w_axis.y
    // w_axis.z
    // mat2: glam::Mat2,
    vec2: Vec2,
    vec3: Vec3,
    vec3a: Vec3A,
    vec4: Vec4,
    mat2: Mat2,
    mat3: Mat3,
    mat3a: Mat3A,
    mat4: Mat4,
    quat: Quat,
    affine2: Affine2,
    affine3a: Affine3A,
    d_vec2: DVec2,
    d_vec3: DVec3,
    d_vec4: DVec4,
    d_mat2: DMat2,
    d_mat3: DMat3,
    d_mat4: DMat4,
    d_quat: DQuat,
    d_affine2: DAffine2,
    d_affine3: DAffine3,
    i8_vec2: I8Vec2,
    i8_vec3: I8Vec3,
    i8_vec4: I8Vec4,
    u8_vec2: U8Vec2,
    u8_vec3: U8Vec3,
    u8_vec4: U8Vec4,
    i16_vec2: I16Vec2,
    i16_vec3: I16Vec3,
    i16_vec4: I16Vec4,
    u16_vec2: U16Vec2,
    u16_vec3: U16Vec3,
    u16_vec4: U16Vec4,
    i_vec2: IVec2,
    i_vec3: IVec3,
    i_vec4: IVec4,
    u_vec2: UVec2,
    u_vec3: UVec3,
    u_vec4: UVec4,
    i64_vec2: I64Vec2,
    i64_vec3: I64Vec3,
    i64_vec4: I64Vec4,
    u64_vec2: U64Vec2,
    u64_vec3: U64Vec3,
    u64_vec4: U64Vec4,
    // usize vecs are in glam but not in bevy::math
    // u_size_vec2: USizeVec2,
    // u_size_vec3: USizeVec3,
    // u_size_vec4: USizeVec4,
    b_vec2: BVec2,
    b_vec3: BVec3,
    b_vec4: BVec4,
}

#[cfg(test)]
mod tests {
    use super::*;
    use bevy::{
        asset::uuid::Uuid,
        prelude::*,
        reflect::{
            GetTypeRegistration, TypeRegistry,
            serde::ReflectSerializer,
        },
    };
    use std::str::FromStr;

    fn snapshot_component_value<
        T: PartialReflect + GetTypeRegistration,
    >(
        value: &T,
        label: &str,
    ) {
        let mut type_registry = TypeRegistry::new();
        type_registry.register::<T>();

        // serialize
        let serializer =
            ReflectSerializer::new(value, &type_registry);

        let mut settings = insta::Settings::clone_current();
        settings.set_snapshot_suffix(label);
        settings.set_prepend_module_to_snapshot(false);
        let _guard = settings.bind_to_scope();
        insta::assert_json_snapshot!(serializer);
    }

    #[test]
    fn key_too_long() {
        let value = ThisIsOverThePythonKeyLengthLimitForBlenderProperties {
            are_you_feeling_it_now_mr_krabs: true,
            im_ready_im_ready_im_ready: "Spongebob".to_string(),
        };

        snapshot_component_value(&value, "key_too_long");
    }

    #[test]
    fn struct_fields() {
        let value = Player {
            name: "Chris Biscardi".to_string(),
            power: 100.,
            test: 4,
        };

        snapshot_component_value(&value, "player");
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

        snapshot_component_value(&value, "team_member");
    }

    #[test]
    fn tuple_struct() {
        let value = ATupleStruct(12);

        snapshot_component_value(&value, "tuple_struct");
    }

    #[test]
    fn multi_element_tuple_struct() {
        let value = MultiElementTupleStruct(
            12,
            Vec3::ZERO,
            2,
            "testing".to_string(),
        );

        snapshot_component_value(
            &value,
            "multi_element_tuple_struct",
        );
    }

    #[test]
    fn marker_component() {
        let value = Marker;

        snapshot_component_value(&value, "marker");
    }

    #[test]
    fn enum_component() {
        let value = TaskPriority::High;

        snapshot_component_value(&value, "task_priority");
    }

    #[test]
    fn enum_component_with_fields() {
        let value = SomeThings::OneThing {
            name: "testing".to_string(),
        };

        snapshot_component_value(
            &value,
            "some_things__one_thing",
        );
    }

    #[test]
    fn enum_component_with_fields_alt() {
        let value = SomeThings::Low(12);

        snapshot_component_value(
            &value,
            "some_things__low",
        );
    }

    #[test]
    fn an_optional_name() {
        let value = AnOptionalName {
            name: Some("A Test Name".to_string()),
        };

        snapshot_component_value(
            &value,
            "an_optional_name__some",
        );

        let value = AnOptionalName { name: None };
        snapshot_component_value(
            &value,
            "an_optional_name__none",
        );
    }

    #[test]
    fn non_zero_numbers() {
        let value = NonZeroNumbers {
            small: std::num::NonZeroU8::new(255).unwrap(),
            an_int: std::num::NonZeroI16::new(-493)
                .unwrap(),
        };
        snapshot_component_value(
            &value,
            "non_zero_numbers",
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

        snapshot_component_value(&value, "bucket_of_types");
    }

    #[test]
    fn enum_component_rich_and_unit_enum() {
        let value = RichAndUnitEnum::Player(Player {
            name: "Chris".to_string(),
            power: 10.,
            test: 42,
        });

        snapshot_component_value(
            &value,
            "rich_and_unit_enum__player",
        );
    }

    #[test]
    fn enum_component_rich_and_unit_enum_alt() {
        let value = RichAndUnitEnum::NotAPlayer;

        snapshot_component_value(
            &value,
            "rich_and_unit_enum__not_a_player",
        );
    }

    #[test]
    fn a_struct_with_color() {
        let value = AStructWithColor {
            base: Color::hsl(20., 50., 50.),
            highlight: Color::oklch(1., 1., 1.),
        };

        snapshot_component_value(
            &value,
            "struct_with_color",
        );
    }

    #[test]
    fn timer_support() {
        let value = TimerContainer(Timer::from_seconds(
            2.,
            TimerMode::Once,
        ));

        snapshot_component_value(&value, "timer_container");
    }

    #[test]
    fn vec3_support() {
        let value = LinearVelocity(Vec3::splat(2.));

        snapshot_component_value(&value, "linear_velocity");
    }

    #[test]
    fn super_glam() {
        let value = SuperGlam {
            vec2: Vec2::default(),
            vec3: Vec3::default(),
            vec3a: Vec3A::default(),
            vec4: Vec4::default(),
            mat2: Mat2::default(),
            mat3: Mat3::default(),
            mat3a: Mat3A::default(),
            mat4: Mat4::default(),
            quat: Quat::default(),
            affine2: Affine2::default(),
            affine3a: Affine3A::default(),
            d_vec2: DVec2::default(),
            d_vec3: DVec3::default(),
            d_vec4: DVec4::default(),
            d_mat2: DMat2::default(),
            d_mat3: DMat3::default(),
            d_mat4: DMat4::default(),
            d_quat: DQuat::default(),
            d_affine2: DAffine2::default(),
            d_affine3: DAffine3::default(),
            i8_vec2: I8Vec2::default(),
            i8_vec3: I8Vec3::default(),
            i8_vec4: I8Vec4::default(),
            u8_vec2: U8Vec2::default(),
            u8_vec3: U8Vec3::default(),
            u8_vec4: U8Vec4::default(),
            i16_vec2: I16Vec2::default(),
            i16_vec3: I16Vec3::default(),
            i16_vec4: I16Vec4::default(),
            u16_vec2: U16Vec2::default(),
            u16_vec3: U16Vec3::default(),
            u16_vec4: U16Vec4::default(),
            i_vec2: IVec2::default(),
            i_vec3: IVec3::default(),
            i_vec4: IVec4::default(),
            u_vec2: UVec2::default(),
            u_vec3: UVec3::default(),
            u_vec4: UVec4::default(),
            i64_vec2: I64Vec2::default(),
            i64_vec3: I64Vec3::default(),
            i64_vec4: I64Vec4::default(),
            u64_vec2: U64Vec2::default(),
            u64_vec3: U64Vec3::default(),
            u64_vec4: U64Vec4::default(),
            // usize vecs are in glam but not in bevy::math
            // u_size_vec2: USizeVec2::default(),
            // u_size_vec3: USizeVec3::default(),
            // u_size_vec4: USizeVec4::default(),
            b_vec2: BVec2::default(),
            b_vec3: BVec3::default(),
            b_vec4: BVec4::default(),
        };

        snapshot_component_value(&value, "all_glam_types");
    }

    // Below this is basically the entire list in /data/list_bevy_components for
    // the current bevy version
    //
    // some types aren't worth trying to represent, such as Material
    // or other Asset Handles. ex: MeshMaterial3d
    // Handles are abstract references to Assets so its unclear
    // what or how they would be useful
    #[test]
    fn animation_player() {
        let value =
            bevy::animation::AnimationPlayer::default();
        snapshot_component_value(&value, "bloom");
    }
    #[test]
    fn animation_target() {
        let value = bevy::animation::AnimationTarget {
            // force a uuid value for testing purposes
            id: bevy::animation::AnimationTargetId(
                Uuid::from_str(
                    "16c27292-862e-4555-af16-d3d8e624c6de",
                )
                .unwrap(),
            ),
            player: Entity::PLACEHOLDER,
        };
        snapshot_component_value(
            &value,
            "animation_target",
        );
    }
    #[test]
    fn animation_graph_handle() {
        let value = bevy::animation::graph::AnimationGraphHandle::default();
        snapshot_component_value(
            &value,
            "animation_graph_handle",
        );
    }
    #[test]
    fn animation_transitions() {
        let value = bevy::animation::transition::AnimationTransitions::default();
        snapshot_component_value(
            &value,
            "animation_transitions",
        );
    }
    #[test]
    fn playback_settings() {
        let value =
            bevy::audio::PlaybackSettings::default();
        snapshot_component_value(
            &value,
            "playback_settings",
        );
    }
    #[test]
    fn spatial_listener() {
        let value = bevy::audio::SpatialListener::default();
        snapshot_component_value(
            &value,
            "spatial_listener",
        );
    }
    #[test]
    fn bloom() {
        let value =
            bevy::core_pipeline::bloom::Bloom::default();
        snapshot_component_value(&value, "bloom");
    }
    #[test]
    fn contrast_adaptive_sharpening() {
        let value = bevy::core_pipeline::contrast_adaptive_sharpening::ContrastAdaptiveSharpening::default();
        snapshot_component_value(
            &value,
            "contrast_adaptive_sharpening",
        );
    }
    #[test]
    fn camera2d() {
        let value = Camera2d::default();
        snapshot_component_value(&value, "camera2d");
    }
    #[test]
    fn camera3d() {
        let value = Camera3d::default();
        snapshot_component_value(&value, "camera3d");
    }
    #[test]
    fn depth_of_field() {
        let value =
            bevy::core_pipeline::dof::DepthOfField::default(
            );
        snapshot_component_value(&value, "depth_of_field");
    }
    #[test]
    fn fxaa() {
        let value =
            bevy::core_pipeline::fxaa::Fxaa::default();
        snapshot_component_value(&value, "bloom");
    }
    #[test]
    fn chromatic_aberration() {
        let value = bevy::core_pipeline::post_process::ChromaticAberration::default();
        snapshot_component_value(
            &value,
            "chromatic_aberration",
        );
    }
    #[test]
    fn deferred_prepass() {
        let value = bevy::core_pipeline::prepass::DeferredPrepass::default();
        snapshot_component_value(
            &value,
            "deferred_prepass",
        );
    }
    #[test]
    fn depth_prepass() {
        let value =
        bevy::core_pipeline::prepass::DepthPrepass::default(
        );
        snapshot_component_value(&value, "depth_prepass");
    }
    #[test]
    fn motion_vector_prepass() {
        let value = bevy::core_pipeline::prepass::MotionVectorPrepass::default();
        snapshot_component_value(
            &value,
            "motion_vector_prepass",
        );
    }
    #[test]
    fn normal_prepass() {
        let value = bevy::core_pipeline::prepass::NormalPrepass::default();
        snapshot_component_value(&value, "normal_prepass");
    }
    #[test]
    fn skybox() {
        let value = bevy::core_pipeline::Skybox::default();
        snapshot_component_value(&value, "skybox");
    }
    #[test]
    fn smaa() {
        let value =
            bevy::core_pipeline::smaa::Smaa::default();
        snapshot_component_value(&value, "smaa");
    }
    #[test]
    fn deband_dither() {
        let value = bevy::core_pipeline::tonemapping::DebandDither::default();
        snapshot_component_value(&value, "deband_dither");
    }
    #[test]
    fn tonemapping() {
        let value = bevy::core_pipeline::tonemapping::Tonemapping::default();
        snapshot_component_value(&value, "tonemapping");
    }
    // child_of:  bevy::ecs::hierarchy::ChildOf,
    // children:  bevy::ecs::hierarchy::Children,
    // name doesn't need to be constructed since its inferred from the blender ui
    // bevy::ecs::name::Name::new("test");
    //
    // we don't need to support gltf extras components, that's the entire point
    // of the rest of the project.
    // gltf_extras:  bevy::gltf::GltfExtras,
    // gltf_material_extras:  bevy::gltf::assets::GltfMaterialExtras,
    // gltf_material_name:  bevy::gltf::assets::GltfMaterialName,
    // gltf_mesh_extras:  bevy::gltf::assets::GltfMeshExtras,
    // gltf_scene_extras:  bevy::gltf::assets::GltfSceneExtras,
    #[test]
    #[should_panic]
    fn gamepad() {
        let value =
            bevy::input::gamepad::Gamepad::default();
        snapshot_component_value(&value, "gamepad");
    }
    #[test]
    fn gamepad_settings() {
        let value =
            bevy::input::gamepad::GamepadSettings::default(
            );
        snapshot_component_value(
            &value,
            "gamepad_settings",
        );
    }
    #[test]
    fn mesh_morph_weights() {
        let value = bevy::render::mesh::morph::MeshMorphWeights::default();
        snapshot_component_value(
            &value,
            "mesh_morph_weights",
        );
    }
    #[test]
    fn morph_weights() {
        let value =
        bevy::render::mesh::morph::MorphWeights::default();
        snapshot_component_value(&value, "morph_weights");
    }
    #[test]
    fn skinned_mesh() {
        let value =
        bevy::render::mesh::skinning::SkinnedMesh::default(
        );
        snapshot_component_value(&value, "skinned_mesh");
    }
    #[test]
    fn cluster_config() {
        let value = bevy::pbr::ClusterConfig::default();
        snapshot_component_value(&value, "cluster_config");
    }
    #[test]
    fn cascades_visible_entities() {
        let value =
            bevy::pbr::CascadesVisibleEntities::default();
        snapshot_component_value(
            &value,
            "cascades_visible_entities",
        );
    }
    #[test]
    fn cubemap_visible_entities() {
        let value =
            bevy::pbr::CubemapVisibleEntities::default();
        snapshot_component_value(
            &value,
            "cubemap_visible_entities",
        );
    }
    #[test]
    fn visible_mesh_entities() {
        let value =
            bevy::pbr::VisibleMeshEntities::default();
        snapshot_component_value(
            &value,
            "visible_mesh_entities",
        );
    }
    // clustered_decal uses Handle<Image>
    // clustered_decal:  bevy::pbr::decal::clustered::ClusteredDecal,
    #[test]
    fn distance_fog() {
        let value = bevy::pbr::DistanceFog::default();
        snapshot_component_value(&value, "distance_fog");
    }
    #[test]
    fn cascade_shadow_config() {
        let value =
            bevy::pbr::CascadeShadowConfig::default();
        snapshot_component_value(
            &value,
            "cascade_shadow_config",
        );
    }
    #[test]
    fn cascades() {
        let value = bevy::pbr::Cascades::default();
        snapshot_component_value(&value, "cascades");
    }
    #[test]
    fn not_shadow_caster() {
        let value = bevy::pbr::NotShadowCaster::default();
        snapshot_component_value(
            &value,
            "not_shadow_caster",
        );
    }
    #[test]
    fn not_shadow_receiver() {
        let value = bevy::pbr::NotShadowReceiver::default();
        snapshot_component_value(
            &value,
            "not_shadow_receiver",
        );
    }
    #[test]
    fn shadow_filtering_method() {
        let value =
            bevy::pbr::ShadowFilteringMethod::default();
        snapshot_component_value(
            &value,
            "shadow_filtering_method",
        );
    }
    #[test]
    fn ambient_light() {
        let value = bevy::pbr::AmbientLight::default();
        snapshot_component_value(&value, "ambient_light");
    }
    #[test]
    fn directional_light() {
        let value = bevy::pbr::DirectionalLight::default();
        snapshot_component_value(
            &value,
            "directional_light",
        );
    }
    #[test]
    fn point_light() {
        let value = bevy::pbr::PointLight::default();
        snapshot_component_value(&value, "point_light");
    }
    #[test]
    fn spot_light() {
        let value = bevy::pbr::SpotLight::default();
        snapshot_component_value(&value, "spot_light");
    }
    #[test]
    fn light_probe() {
        let value = bevy::pbr::LightProbe::default();
        snapshot_component_value(&value, "light_probe");
    }
    #[test]
    fn environment_map_light() {
        let value = bevy::pbr::environment_map::EnvironmentMapLight::default();
        snapshot_component_value(
            &value,
            "environment_map_light",
        );
    }
    #[test]
    fn irradiance_volume() {
        let value = bevy::pbr::irradiance_volume::IrradianceVolume::default();
        snapshot_component_value(
            &value,
            "irradiance_volume",
        );
    }
    //   bevy_pbr::mesh_material::MeshMaterial3d<bevy_pbr::extended_material::ExtendedMaterial<bevy_pbr::pbr_material::StandardMaterial, bevy_pbr::decal::forward::ForwardDecalMaterialExt>>,
    //   bevy_pbr::mesh_material::MeshMaterial3d<bevy_pbr::pbr_material::StandardMaterial>,
    #[test]
    fn screen_space_ambient_occlusion() {
        let value =
            bevy::pbr::ScreenSpaceAmbientOcclusion::default(
            );
        snapshot_component_value(
            &value,
            "screen_space_ambient_occlusion",
        );
    }
    #[test]
    fn screen_space_reflections() {
        let value =
            bevy::pbr::ScreenSpaceReflections::default();
        snapshot_component_value(
            &value,
            "screen_space_reflections",
        );
    }
    #[test]
    fn volumetric_fog() {
        let value = bevy::pbr::VolumetricFog::default();
        snapshot_component_value(&value, "volumetric_fog");
    }
    #[test]
    fn volumetric_light() {
        let value = bevy::pbr::VolumetricLight::default();
        snapshot_component_value(
            &value,
            "volumetric_light",
        );
    }
    #[test]
    fn pickable() {
        let value = bevy::picking::Pickable::default();
        snapshot_component_value(&value, "pickable");
    }
    #[test]
    fn picking_interaction() {
        let value =
        bevy::picking::hover::PickingInteraction::default();
        snapshot_component_value(
            &value,
            "picking_interaction",
        );
    }
    #[test]
    fn pointer_id() {
        let value =
            bevy::picking::pointer::PointerId::default();
        snapshot_component_value(&value, "pointer_id");
    }
    #[test]
    fn pointer_interaction() {
        let value =
        bevy::picking::pointer::PointerInteraction::default(
        );
        snapshot_component_value(
            &value,
            "pointer_interaction",
        );
    }
    #[test]
    fn pointer_location() {
        let value =
        bevy::picking::pointer::PointerLocation::default();
        snapshot_component_value(
            &value,
            "pointer_location",
        );
    }
    #[test]
    fn pointer_press() {
        let value =
            bevy::picking::pointer::PointerPress::default();
        snapshot_component_value(&value, "pointer_press");
    }
    #[test]
    fn camera() {
        let value = bevy::render::camera::Camera::default();
        snapshot_component_value(&value, "camera");
    }
    // camera_main_texture_usages doesn't implement `ReflectSerialize` or `ReflectSerializeWithRegistry`
    // camera_main_texture_usages:  bevy::render::camera::CameraMainTextureUsages,
    // camera_render_graph:  bevy::render::camera::CameraRenderGraph,
    // exposure doesn't implement `ReflectSerialize` or `ReflectSerializeWithRegistry`
    // exposure:  bevy::render::camera::Exposure,
    #[test]
    fn mip_bias() {
        let value =
            bevy::render::camera::MipBias::default();
        snapshot_component_value(&value, "mip_bias");
    }
    #[test]
    fn temporal_jitter() {
        let value =
            bevy::render::camera::TemporalJitter::default();
        snapshot_component_value(&value, "temporal_jitter");
    }
    #[test]
    fn manual_texture_view_handle() {
        let value = bevy::render::camera::ManualTextureViewHandle::default();
        snapshot_component_value(
            &value,
            "manual_texture_view_handle",
        );
    }
    #[test]
    fn projection() {
        let value =
            bevy::render::camera::Projection::default();
        snapshot_component_value(&value, "projection");
    }
    #[test]
    fn occlusion_culling() {
        let value = bevy::render::experimental::occlusion_culling::OcclusionCulling::default();
        snapshot_component_value(
            &value,
            "occlusion_culling",
        );
    }
    #[test]
    fn mesh2d() {
        let value = bevy::render::mesh::Mesh2d::default();
        snapshot_component_value(&value, "mesh2d");
    }
    #[test]
    fn mesh3d() {
        let value = bevy::render::mesh::Mesh3d::default();
        snapshot_component_value(&value, "mesh3d");
    }
    #[test]
    fn aabb() {
        let value =
            bevy::render::primitives::Aabb::default();
        snapshot_component_value(&value, "aabb");
    }
    #[test]
    fn cascades_frusta() {
        let value =
        bevy::render::primitives::CascadesFrusta::default();
        snapshot_component_value(&value, "cascades_frusta");
    }
    #[test]
    fn cubemap_frusta() {
        let value =
        bevy::render::primitives::CubemapFrusta::default();
        snapshot_component_value(&value, "cubemap_frusta");
    }
    #[test]
    fn frustum() {
        let value =
            bevy::render::primitives::Frustum::default();
        snapshot_component_value(&value, "frustum");
    }
    #[test]
    fn sync_to_render_world() {
        let value = bevy::render::sync_world::SyncToRenderWorld::default();
        snapshot_component_value(
            &value,
            "sync_to_render_world",
        );
    }
    // Range doesn't implement `ReflectSerialize` or `ReflectSerializeWithRegistry`
    // and Range is used in color_grading
    // color_grading:  bevy::render::view::ColorGrading,
    #[test]
    fn msaa() {
        let value = bevy::render::view::Msaa::default();
        snapshot_component_value(&value, "msaa");
    }
    #[test]
    fn inherited_visibility() {
        let value = bevy::render::view::visibility::InheritedVisibility::default();
        snapshot_component_value(
            &value,
            "inherited_visibility",
        );
    }
    #[test]
    fn no_frustum_culling() {
        let value = bevy::render::view::visibility::NoFrustumCulling::default();
        snapshot_component_value(
            &value,
            "no_frustum_culling",
        );
    }
    #[test]
    fn view_visibility() {
        let value = bevy::render::view::visibility::ViewVisibility::default();
        snapshot_component_value(&value, "view_visibility");
    }
    #[test]
    fn visibility() {
        let value =
        bevy::render::view::visibility::Visibility::default(
        );
        snapshot_component_value(&value, "visibility");
    }
    #[test]
    fn visibility_class() {
        let value = bevy::render::view::visibility::VisibilityClass::default();
        snapshot_component_value(
            &value,
            "visibility_class",
        );
    }
    #[test]
    fn visible_entities() {
        let value = bevy::render::view::visibility::VisibleEntities::default();
        snapshot_component_value(
            &value,
            "visible_entities",
        );
    }
    // Range doesn't implement `ReflectSerialize` or `ReflectSerializeWithRegistry`
    // and Range is used in visibility_range
    // TODO: this is a useful type that we should figure out how to support
    // visibility_range:  bevy::render::view::visibility::VisibilityRange,
    #[test]
    fn render_layers() {
        let value = bevy::render::view::visibility::RenderLayers::default();
        snapshot_component_value(&value, "render_layers");
    }
    // screenshot:  bevy::render::view::window::screenshot::Screenshot,
    #[test]
    fn dynamic_scene_root() {
        let value =
            bevy::scene::DynamicSceneRoot::default();
        snapshot_component_value(
            &value,
            "dynamic_scene_root",
        );
    }
    #[test]
    fn scene_root() {
        let value = bevy::scene::SceneRoot::default();
        snapshot_component_value(&value, "scene_root");
    }
    //   bevy_sprite::mesh2d::material::MeshMaterial2d<bevy_sprite::mesh2d::color_material::ColorMaterial>,
    #[test]
    fn sprite_picking_camera() {
        let value =
            bevy::sprite::SpritePickingCamera::default();
        snapshot_component_value(
            &value,
            "sprite_picking_camera",
        );
    }
    #[test]
    fn anchor() {
        let value = bevy::sprite::Anchor::default();
        snapshot_component_value(&value, "anchor");
    }
    #[test]
    fn sprite() {
        let value = bevy::sprite::Sprite::default();
        snapshot_component_value(&value, "sprite");
    }
    #[test]
    fn text_bounds() {
        let value = bevy::text::TextBounds::default();
        snapshot_component_value(&value, "text_bounds");
    }
    #[test]
    fn text_layout_info() {
        let value = bevy::text::TextLayoutInfo::default();
        snapshot_component_value(
            &value,
            "text_layout_info",
        );
    }
    #[test]
    fn text2d() {
        let value = bevy::text::Text2d::default();
        snapshot_component_value(&value, "text2d");
    }
    #[test]
    fn computed_text_block() {
        let value =
            bevy::text::ComputedTextBlock::default();
        snapshot_component_value(
            &value,
            "computed_text_block",
        );
    }
    #[test]
    fn text_color() {
        let value = bevy::text::TextColor::default();
        snapshot_component_value(&value, "text_color");
    }
    #[test]
    fn text_font() {
        let value = bevy::text::TextFont::default();
        snapshot_component_value(&value, "text_font");
    }
    #[test]
    fn text_layout() {
        let value = bevy::text::TextLayout::default();
        snapshot_component_value(&value, "text_layout");
    }
    #[test]
    fn text_span() {
        let value = bevy::text::TextSpan::default();
        snapshot_component_value(&value, "text_span");
    }
    #[test]
    fn global_transform() {
        let value = bevy::transform::components::GlobalTransform::default();
        snapshot_component_value(
            &value,
            "global_transform",
        );
    }
    #[test]
    fn transform() {
        let value =
            bevy::transform::components::Transform::default(
            );
        snapshot_component_value(&value, "transform");
    }
    #[test]
    fn transform_tree_changed() {
        let value = bevy::transform::components::TransformTreeChanged::default();
        snapshot_component_value(
            &value,
            "transform_tree_changed",
        );
    }
    #[test]
    fn focus_policy() {
        let value = bevy::ui::FocusPolicy::default();
        snapshot_component_value(&value, "focus_policy");
    }
    #[test]
    fn interaction() {
        let value = bevy::ui::Interaction::default();
        snapshot_component_value(&value, "interaction");
    }
    #[test]
    fn relative_cursor_position() {
        let value =
            bevy::ui::RelativeCursorPosition::default();
        snapshot_component_value(
            &value,
            "relative_cursor_position",
        );
    }
    #[test]
    fn content_size() {
        let value =
            bevy::ui::measurement::ContentSize::default();
        snapshot_component_value(&value, "content_size");
    }
    #[test]
    fn ui_picking_camera() {
        let value =
        bevy::ui::picking_backend::UiPickingCamera::default(
        );
        snapshot_component_value(
            &value,
            "ui_picking_camera",
        );
    }
    #[test]
    fn background_color() {
        let value = bevy::ui::BackgroundColor::default();
        snapshot_component_value(
            &value,
            "background_color",
        );
    }
    #[test]
    fn border_color() {
        let value = bevy::ui::BorderColor::default();
        snapshot_component_value(&value, "border_color");
    }
    #[test]
    fn border_radius() {
        let value = bevy::ui::BorderRadius::default();
        snapshot_component_value(&value, "border_radius");
    }
    #[test]
    fn box_shadow() {
        let value = bevy::ui::BoxShadow::default();
        snapshot_component_value(&value, "box_shadow");
    }
    #[test]
    fn box_shadow_samples() {
        let value = bevy::ui::BoxShadowSamples::default();
        snapshot_component_value(
            &value,
            "box_shadow_samples",
        );
    }
    #[test]
    fn calculated_clip() {
        let value = bevy::ui::CalculatedClip::default();
        snapshot_component_value(&value, "calculated_clip");
    }
    #[test]
    fn computed_node() {
        let value = bevy::ui::ComputedNode::default();
        snapshot_component_value(&value, "computed_node");
    }
    #[test]
    fn computed_node_target() {
        let value = bevy::ui::ComputedNodeTarget::default();
        snapshot_component_value(
            &value,
            "computed_node_target",
        );
    }
    #[test]
    fn node() {
        let value = bevy::ui::Node::default();
        snapshot_component_value(&value, "node");
    }
    #[test]
    fn outline() {
        let value = bevy::ui::Outline::default();
        snapshot_component_value(&value, "outline");
    }
    #[test]
    fn scroll_position() {
        let value = bevy::ui::ScrollPosition::default();
        snapshot_component_value(&value, "scroll_position");
    }
    #[test]
    fn text_shadow() {
        let value = bevy::ui::TextShadow::default();
        snapshot_component_value(&value, "text_shadow");
    }
    #[test]
    fn ui_anti_alias() {
        let value = bevy::ui::UiAntiAlias::default();
        snapshot_component_value(&value, "ui_anti_alias");
    }
    #[test]
    fn ui_target_camera() {
        let value = UiTargetCamera(Entity::PLACEHOLDER);
        snapshot_component_value(
            &value,
            "ui_target_camera",
        );
    }
    #[test]
    fn z_index() {
        let value = bevy::ui::ZIndex::default();
        snapshot_component_value(&value, "z_index");
    }
    #[test]
    fn button() {
        let value = bevy::ui::widget::Button::default();
        snapshot_component_value(&value, "button");
    }
    #[test]
    fn image_node() {
        let value = bevy::ui::widget::ImageNode::default();
        snapshot_component_value(&value, "image_node");
    }
    #[test]
    fn image_node_size() {
        let value =
            bevy::ui::widget::ImageNodeSize::default();
        snapshot_component_value(&value, "image_node_size");
    }
    #[test]
    fn label() {
        let value = bevy::ui::widget::Label::default();
        snapshot_component_value(&value, "label");
    }
    #[test]
    fn text() {
        let value = bevy::ui::widget::Text::default();
        snapshot_component_value(&value, "text");
    }
    #[test]
    fn text_node_flags() {
        let value =
            bevy::ui::widget::TextNodeFlags::default();
        snapshot_component_value(&value, "text_node_flags");
    }
    #[test]
    fn monitor() {
        let value = bevy::window::Monitor {
            name: Some(
                "Probably dont use Monitor in Blender lol"
                    .to_string(),
            ),
            physical_height: 1920,
            physical_width: 1080,
            physical_position: IVec2::ZERO,
            refresh_rate_millihertz: Some(60),
            scale_factor: 1.,
            video_modes: vec![bevy::window::VideoMode {
                physical_size: UVec2::new(1920, 1080),
                bit_depth: 8,
                refresh_rate_millihertz: 10,
            }],
        };
        snapshot_component_value(&value, "monitor");
    }
    #[test]
    fn primary_window() {
        let value = bevy::window::PrimaryWindow::default();
        snapshot_component_value(&value, "primary_window");
    }
    #[test]
    fn window() {
        let value = bevy::window::Window::default();
        snapshot_component_value(&value, "window");
    }
    #[test]
    fn cursor_icon() {
        let value =
            bevy::winit::cursor::CursorIcon::default();
        snapshot_component_value(&value, "cursor_icon");
    }
}
