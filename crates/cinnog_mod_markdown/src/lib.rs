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
use gray_matter::{Matter, engine::YAML};
use serde::de::DeserializeOwned;
use std::{
    fs::{self, read_to_string},
    io::{self, Cursor},
    marker::PhantomData,
    path::Path,
};
#[cfg(feature = "generator")]
use syntect::highlighting::ThemeSet;
// comrak
#[cfg(feature = "generator")]
use comrak::{
    ComrakPlugins, Options, markdown_to_html_with_plugins,
    plugins::syntect::SyntectAdapterBuilder,
};

#[cfg(feature = "generator")]
const NIGHT_OWL: &[u8; 27913] =
    include_bytes!("./night-owlish.tmtheme");

/// System sets related to markdown and markdown
/// to HTML conversion
#[derive(SystemSet, Clone, Debug, PartialEq, Eq, Hash)]
pub enum MarkdownSystems {
    /// System sets for systems reading markdown
    /// files
    Read,
    /// System set for systems converting markdown
    /// to HTML
    Convert,
}

struct ReadMarkdown<
    M: Ingest + DeserializeOwned + Sync + Send + 'static,
> {
    _marker: PhantomData<M>,
}

impl<M: Ingest + DeserializeOwned + Sync + Send + 'static>
    Plugin for ReadMarkdown<M>
{
    fn build(&self, app: &mut App) {
        app.add_systems(
            Update,
            read_markdown_from_directories::<M>
                .in_set(MarkdownSystems::Read),
        );
    }
}

impl<M: Ingest + DeserializeOwned + Sync + Send + 'static>
    ReadMarkdown<M>
{
    pub fn new() -> Self {
        Self {
            _marker: PhantomData,
        }
    }
}

/// Extension trait for the data layer containing
/// markdown specific methods
pub trait MarkdownDataLayer {
    /// Add a directory to be loaded as a
    /// collection of markdown files
    fn add_custom_markdown_directory<
        M: Ingest + DeserializeOwned + Sync + Send + 'static,
    >(
        &mut self,
        directory: impl Into<String>,
    ) -> &mut Self;
}

#[cfg(feature = "generator")]
impl MarkdownDataLayer for Generator {
    fn add_custom_markdown_directory<
        M: Ingest + DeserializeOwned + Sync + Send + 'static,
    >(
        &mut self,
        directory: impl Into<String>,
    ) -> &mut Self {
        self.app.init_resource::<MarkdownDirectories<M>>();
        if !self.app.is_plugin_added::<ReadMarkdown<M>>() {
            self.add_plugins(ReadMarkdown::<M>::new());
        }

        let mut directories =
            self.app
                .world_mut()
                .resource_mut::<MarkdownDirectories<M>>();
        directories.directories.push(directory.into());

        self
    }
}

#[derive(Resource)]
struct MarkdownDirectories<
    M: Ingest + DeserializeOwned + Sync + Send + 'static,
> {
    directories: Vec<String>,
    _marker: PhantomData<M>,
}

impl<M: Ingest + DeserializeOwned + Sync + Send + 'static>
    Default for MarkdownDirectories<M>
{
    fn default() -> Self {
        Self {
            directories: vec![],
            _marker: PhantomData,
        }
    }
}

fn read_markdown_from_directories<
    FrontMatter: Ingest + DeserializeOwned + Sync + Send + 'static,
>(
    mut commands: Commands,
    directories: Res<MarkdownDirectories<FrontMatter>>,
) {
    fn read_from_dir<
        FrontMatter: Ingest + DeserializeOwned + Sync + Send + 'static,
    >(
        path: &Path,
        commands: &mut Commands,
    ) -> io::Result<Vec<Entity>> {
        let mut files = vec![];

        for entry in fs::read_dir(path)? {
            let entry = entry?;
            let path = entry.path();
            if path.is_file() {
                files.push(read_markdown::<FrontMatter>(
                    &path, commands,
                )?);
            } else if path.is_dir() {
                files.append(&mut read_from_dir::<
                    FrontMatter,
                >(
                    &path, commands
                )?)
            }
        }
        Ok(files)
    }
    for directory in &directories.directories {
        let path = Path::new(directory);
        read_from_dir::<FrontMatter>(path, &mut commands)
            .unwrap_or_else(|e| {
                panic!(
                    "Failed to read files from {}: {:?}",
                    directory, e
                )
            });
    }
}

fn read_markdown<
    FrontMatter: Ingest + DeserializeOwned + Sync + Send + 'static,
>(
    path: &Path,
    commands: &mut Commands,
) -> io::Result<Entity> {
    let file = read_to_string(path)?;
    let matter = Matter::<YAML>::new();
    let markdown = matter.parse(&file);
    let mut file = commands.spawn(());
    if let Some(front_matter) = markdown.data {
        let parsed_front_matter =
            front_matter.deserialize::<FrontMatter>()?;
        parsed_front_matter.ingest_path(&mut file, path);
        parsed_front_matter.ingest(&mut file);
    }
    file.insert(MarkdownBody(markdown.content));
    Ok(file.id())
}

/// Component containing Markdown
#[derive(Component, Clone)]
pub struct MarkdownBody(pub String);

/// Plugin to convert all markdown content to HTML
///
/// The plugin will query for all [`MarkdownBody`]
/// components and add a [`Html`] component to
/// each of the entities.
pub struct ConvertMarkdownToHtml;

#[cfg(feature = "generator")]
impl Plugin for ConvertMarkdownToHtml {
    fn build(&self, app: &mut App) {
        app.configure_sets(
            Update,
            (
                MarkdownSystems::Read,
                MarkdownSystems::Convert,
            )
                .chain(),
        )
        .add_systems(
            Update,
            convert_markdown_to_html
                .in_set(MarkdownSystems::Convert),
        );
    }
}

#[cfg(feature = "generator")]
fn convert_markdown_to_html(
    markdown: Query<(Entity, &MarkdownBody)>,
    mut commands: Commands,
) {
    let mut cursor = Cursor::new(NIGHT_OWL);

    let theme_night_owl =
        ThemeSet::load_from_reader(&mut cursor)
            .expect("expect markdown theme to be loadable");
    let mut theme_set = ThemeSet::new();
    theme_set
        .themes
        .entry("Night Owl".to_string())
        .or_insert(theme_night_owl);

    let value = SyntectAdapterBuilder::new()
        .theme_set(theme_set)
        .theme("Night Owl");
    let adapter = value.build();

    for (file, MarkdownBody(markdown)) in &markdown {
        let mut plugins = ComrakPlugins::default();
        plugins.render.codefence_syntax_highlighter =
            Some(&adapter);
        let mut options = Options::default();
        // UNSAFE HTML TAGS!
        // options.render.unsafe_ = true;
        // extensions, like those on github
        options.extension.strikethrough = true;
        options.extension.tagfilter = true;
        options.extension.table = true;
        options.extension.autolink = false;
        options.extension.tasklist = true;
        options.extension.superscript = true;
        options.extension.header_ids = Some("".to_string());
        options.extension.footnotes = true;
        options.extension.description_lists = false;
        options.extension.front_matter_delimiter = None;
        options.extension.multiline_block_quotes = true;
        options.extension.alerts = true;

        plugins.render.codefence_syntax_highlighter =
            Some(&adapter);

        let formatted = markdown_to_html_with_plugins(
            markdown, &options, &plugins,
        );

        commands.entity(file).insert(Html(formatted));
    }
}

/// Component containing HTML
#[derive(Component, Clone)]
pub struct Html(pub String);
