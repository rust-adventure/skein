use bevy_reflect::{Reflect, prelude::*};
/// Components that are meant to be used by Skein internally.
/// These re-use the same reflection infrastructure everything else
/// does, but let Skein handle the data before the application sees it

/// An image sampler that is used for `Handle<Image>` support
/// in the Blender addon. We use this to construct the appropriate
/// Bevy value, since `bevy_image::image::ImageSampler` does not
/// implement `Reflect`
/// How edges should be handled in texture addressing.
///
/// See [`ImageSamplerDescriptor`] for information how to configure this.
///
/// This type mirrors [`AddressMode`].
#[derive(
    Clone, Copy, Debug, Default, PartialEq, Reflect,
)]
#[reflect(Clone, Debug)]
pub enum ImageAddressMode {
    /// Clamp the value to the edge of the texture.
    ///
    /// -0.25 -> 0.0
    /// 1.25  -> 1.0
    #[default]
    ClampToEdge,
    /// Repeat the texture in a tiling fashion.
    ///
    /// -0.25 -> 0.75
    /// 1.25 -> 0.25
    Repeat,
    /// Repeat the texture, mirroring it every repeat.
    ///
    /// -0.25 -> 0.25
    /// 1.25 -> 0.75
    MirrorRepeat,
    /// Clamp the value to the border of the texture
    /// Requires the wgpu feature [`Features::ADDRESS_MODE_CLAMP_TO_BORDER`].
    ///
    /// -0.25 -> border
    /// 1.25 -> border
    ClampToBorder,
}

/// Texel mixing mode when sampling between texels.
///
/// This type mirrors [`FilterMode`].
#[derive(
    Clone, Copy, Debug, Default, PartialEq, Reflect,
)]
#[reflect(Clone, Debug)]
pub enum ImageFilterMode {
    /// Nearest neighbor sampling.
    ///
    /// This creates a pixelated effect when used as a mag filter.
    #[default]
    Nearest,
    /// Linear Interpolation.
    ///
    /// This makes textures smooth but blurry when used as a mag filter.
    Linear,
}

/// Comparison function used for depth and stencil operations.
///
/// This type mirrors [`CompareFunction`].
#[derive(Clone, Copy, Debug, PartialEq, Reflect)]
#[reflect(Clone, Debug)]
pub enum ImageCompareFunction {
    /// Function never passes
    Never,
    /// Function passes if new value less than existing value
    Less,
    /// Function passes if new value is equal to existing value. When using
    /// this compare function, make sure to mark your Vertex Shader's `@builtin(position)`
    /// output as `@invariant` to prevent artifacting.
    Equal,
    /// Function passes if new value is less than or equal to existing value
    LessEqual,
    /// Function passes if new value is greater than existing value
    Greater,
    /// Function passes if new value is not equal to existing value. When using
    /// this compare function, make sure to mark your Vertex Shader's `@builtin(position)`
    /// output as `@invariant` to prevent artifacting.
    NotEqual,
    /// Function passes if new value is greater than or equal to existing value
    GreaterEqual,
    /// Function always passes
    Always,
}

/// Color variation to use when the sampler addressing mode is [`ImageAddressMode::ClampToBorder`].
///
/// This type mirrors [`SamplerBorderColor`].
#[derive(Clone, Copy, Debug, PartialEq, Reflect)]
#[reflect(Clone, Debug)]
pub enum ImageSamplerBorderColor {
    /// RGBA color `[0, 0, 0, 0]`.
    TransparentBlack,
    /// RGBA color `[0, 0, 0, 1]`.
    OpaqueBlack,
    /// RGBA color `[1, 1, 1, 1]`.
    OpaqueWhite,
    /// On the Metal wgpu backend, this is equivalent to [`Self::TransparentBlack`] for
    /// textures that have an alpha component, and equivalent to [`Self::OpaqueBlack`]
    /// for textures that do not have an alpha component. On other backends,
    /// this is equivalent to [`Self::TransparentBlack`]. Requires
    /// [`Features::ADDRESS_MODE_CLAMP_TO_ZERO`]. Not supported on the web.
    Zero,
}

/// Indicates to an `ImageLoader` how an [`Image`] should be sampled.
///
/// As this type is part of the `ImageLoaderSettings`,
/// it will be serialized to an image asset `.meta` file which might require a migration in case of
/// a breaking change.
///
/// This types mirrors [`SamplerDescriptor`], but that might change in future versions.
#[derive(Clone, Debug, PartialEq, Reflect)]
#[reflect(Clone, Debug)]
pub struct ImageSamplerDescriptor {
    pub label: Option<String>,
    /// How to deal with out of bounds accesses in the u (i.e. x) direction.
    pub address_mode_u: ImageAddressMode,
    /// How to deal with out of bounds accesses in the v (i.e. y) direction.
    pub address_mode_v: ImageAddressMode,
    /// How to deal with out of bounds accesses in the w (i.e. z) direction.
    pub address_mode_w: ImageAddressMode,
    /// How to filter the texture when it needs to be magnified (made larger).
    pub mag_filter: ImageFilterMode,
    /// How to filter the texture when it needs to be minified (made smaller).
    pub min_filter: ImageFilterMode,
    /// How to filter between mip map levels
    pub mipmap_filter: ImageFilterMode,
    /// Minimum level of detail (i.e. mip level) to use.
    pub lod_min_clamp: f32,
    /// Maximum level of detail (i.e. mip level) to use.
    pub lod_max_clamp: f32,
    /// If this is enabled, this is a comparison sampler using the given comparison function.
    pub compare: Option<ImageCompareFunction>,
    /// Must be at least 1. If this is not 1, all filter modes must be linear.
    pub anisotropy_clamp: u16,
    /// Border color to use when `address_mode` is [`ImageAddressMode::ClampToBorder`].
    pub border_color: Option<ImageSamplerBorderColor>,
}

impl Default for ImageSamplerDescriptor {
    fn default() -> Self {
        Self {
            address_mode_u: Default::default(),
            address_mode_v: Default::default(),
            address_mode_w: Default::default(),
            mag_filter: Default::default(),
            min_filter: Default::default(),
            mipmap_filter: Default::default(),
            lod_min_clamp: 0.0,
            lod_max_clamp: 32.0,
            compare: None,
            anisotropy_clamp: 1,
            border_color: None,
            label: None,
        }
    }
}

#[derive(Debug, Default, Clone, PartialEq, Reflect)]
#[reflect(Default, Debug, Clone)]
pub enum ImageSampler {
    /// Default image sampler, derived from the `ImagePlugin` setup.
    #[default]
    Default,
    /// Custom sampler for this image which will override global default.
    Descriptor(ImageSamplerDescriptor),
}
