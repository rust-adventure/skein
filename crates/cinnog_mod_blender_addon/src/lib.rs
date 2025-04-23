use bevy_app::{App, Plugin, Update};
use bevy_ecs::{
    component::Component,
    entity::Entity,
    prelude::{Commands, Query, Resource},
    schedule::{
        IntoSystemConfigs, IntoSystemSetConfigs, SystemSet,
    },
    system::Res,
};
use cinnog::Ingest;
#[cfg(feature = "generator")]
use cinnog::generator::Generator;
use serde::{Deserialize, Serialize, de::DeserializeOwned};
use std::{
    fs::{self, read_to_string},
    io,
    path::Path,
};
#[cfg(feature = "generator")]
use zip;

/// System sets related to markdown and markdown
/// to HTML conversion
#[derive(SystemSet, Clone, Debug, PartialEq, Eq, Hash)]
pub enum BlenderZipSystems {
    /// System sets for systems reading markdown
    /// files
    Read,
    /// System set for systems converting markdown
    /// to HTML
    Convert,
}

struct ReadBlenderZips;

#[cfg(feature = "generator")]
impl Plugin for ReadBlenderZips {
    fn build(&self, app: &mut App) {
        app.add_systems(
            Update,
            read_zip_from_directories
                .in_set(BlenderZipSystems::Read),
        );
    }
}

/// Extension trait for the data layer containing
/// markdown specific methods
pub trait BlenderAddonZipDataLayer {
    /// Add a directory to be loaded as a
    /// collection of markdown files
    fn add_blender_addon_zips_directory(
        &mut self,
        directory: impl Into<String>,
    ) -> &mut Self;
}

#[cfg(feature = "generator")]
impl BlenderAddonZipDataLayer for Generator {
    fn add_blender_addon_zips_directory(
        &mut self,
        directory: impl Into<String>,
    ) -> &mut Self {
        self.app.init_resource::<BlenderAddonDirectories>();
        if !self.app.is_plugin_added::<ReadBlenderZips>() {
            self.add_plugins(ReadBlenderZips);
        }

        let mut directories =
            self.app
                .world_mut()
                .resource_mut::<BlenderAddonDirectories>();
        directories.directories.push(directory.into());

        self
    }
}

#[derive(Resource)]
struct BlenderAddonDirectories {
    directories: Vec<String>,
}

impl Default for BlenderAddonDirectories {
    fn default() -> Self {
        Self {
            directories: vec![],
        }
    }
}

#[cfg(feature = "generator")]
fn read_zip_from_directories(
    mut commands: Commands,
    directories: Res<BlenderAddonDirectories>,
) {
    fn read_from_dir(
        path: &Path,
        commands: &mut Commands,
    ) -> io::Result<Vec<Entity>> {
        use walkdir::{DirEntry, WalkDir};

        fn is_hidden(entry: &DirEntry) -> bool {
            entry
                .file_name()
                .to_str()
                .map(|s| s.starts_with("."))
                .unwrap_or(false)
        }

        let walker = WalkDir::new(path).into_iter();
        let files = walker
            .filter_entry(|e| !is_hidden(e))
            .filter_map(|entry| entry.ok())
            .filter(|entry| {
                entry
                    .path()
                    .extension()
                    .is_some_and(|ext| ext == "zip")
            })
            .filter_map(|entry| {
                read_manifest(&entry.path(), commands).ok()
            })
            .collect();

        Ok(files)
    }
    for directory in &directories.directories {
        let path = Path::new(directory);
        read_from_dir(path, &mut commands).unwrap_or_else(
            |e| {
                panic!(
                    "Failed to read files from {}: {:?}",
                    directory, e
                )
            },
        );
    }
}

#[cfg(feature = "generator")]
fn read_manifest(
    path: &Path,
    commands: &mut Commands,
) -> io::Result<Entity> {
    use std::io::Read;

    let file = fs::File::open(path)?;
    let mut zip = zip::ZipArchive::new(file)?;

    let mut zipfile =
        zip.by_name("blender_manifest.toml")?;
    let mut content = String::new();
    zipfile.read_to_string(&mut content)?;

    let manifest: BlenderManifest =
        toml::from_str(&content).map_err(|e| {
            io::Error::new(
                io::ErrorKind::Other,
                "couldn't parse blender_manifest",
            )
        })?;
    let mut file = commands.spawn(());
    file.insert((ManifestBody(content), manifest));
    Ok(file.id())
}

/// Component containing Markdown
#[derive(Component, Clone)]
pub struct ManifestBody(pub String);

/// Component containing The Manifest information
#[derive(Component, Clone, Serialize, Deserialize)]
pub struct BlenderManifest {
    pub id: String,
    pub version: semver::Version,
    pub name: String,
    pub tagline: String,
    pub maintainer: String,
    pub tags: Vec<String>,
    pub blender_version_min: Option<semver::Version>,
    pub blender_version_max: Option<semver::Version>,
}

#[derive(
    Debug, Component, Clone, Serialize, Deserialize,
)]
pub struct BlenderManifestUi {
    pub id: String,
    pub version: String,
    pub name: String,
    pub tagline: String,
    pub maintainer: String,
    pub tags: Vec<String>,
    pub blender_version_min: Option<String>,
    pub blender_version_max: Option<String>,
}

impl BlenderManifest {
    pub fn to_ui_repr(&self) -> BlenderManifestUi {
        BlenderManifestUi {
            version: self.version.to_string(),
            blender_version_min: self
                .blender_version_min
                .as_ref()
                .map(|version| version.to_string()),
            blender_version_max: self
                .blender_version_max
                .as_ref()
                .map(|version| version.to_string()),
            id: self.id.clone(),
            name: self.name.clone(),
            tagline: self.tagline.clone(),
            maintainer: self.maintainer.clone(),
            tags: self.tags.clone(),
        }
    }
}

impl BlenderManifestUi {
    pub fn release_install_url(&self) -> String {
        let BlenderManifestUi { id, version, .. } = self;
        format!(
            "/releases/{id}-{version}.zip?repository=.%2Findex.json"
        )
    }
}
