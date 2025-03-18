use app::{
    pages::{
        blog_post, doc_post,
        home_page::{Age, PersonName},
    },
    shell, NavItem, NavLink, NavigationItems, SiteName,
};
use bevy_ecs::system::EntityCommands;
use cinnog::{
    default_bundle_from_path,
    generator::Generator,
    loaders::{
        markdown::{
            ConvertMarkdownToHtml, MarkdownDataLayer,
        },
        ron::RonDataLayer,
    },
    Ingest,
};
use cinnog_mod_markdown::MarkdownDataLayer as _;
use leptos::serde;
use std::{io, path::Path};

#[tokio::main]
async fn main() -> io::Result<()> {
    let navigation = vec![
        NavItem {
            title: "Introduction",
            links: vec![
                NavLink {
                    title: "Getting started",
                    href: "/",
                },
                NavLink {
                    title: "Installation",
                    href: "/docs/installation",
                },
            ],
        },
        NavItem {
            title: "The Blender Addon",
            links: vec![
                NavLink {
                    title: "Bevy Remote Protocol",
                    href: "/docs/bevy-remote-protocol",
                },
                NavLink {
                    title: "Inserting a Component",
                    href: "/docs/inserting-a-component",
                },
                NavLink {
                    title: "Components on Materials",
                    href: "/docs/components-on-objects",
                },
                NavLink {
                    title: "Components on Meshes",
                    href: "/docs/components-on-meshes",
                },
                NavLink {
                    title: "Components on Materials",
                    href: "/docs/components-on-materials",
                },
                NavLink {
                    title: "Using Blender Drivers",
                    href: "/docs/using-blender-drivers",
                },
                NavLink {
                    title: "Collection Instances",
                    href: "/docs/collection-instances",
                },
            ],
        },
        NavItem {
            title: "Contributing",
            links: vec![
                NavLink {
                    title: "Overview",
                    href: "/docs/contributing",
                },
                NavLink {
                    title: "Blender Addon Structure",
                    href: "/docs/blender-addon-structure",
                },
                NavLink {
                    title: "Property Groups",
                    href: "/docs/property-groups",
                },
                NavLink {
                    title: "Testing",
                    href: "/docs/testing",
                },
            ],
        },
        NavItem {
            title: "Use Cases",
            links: vec![
                NavLink {
                    title: "Build a Level",
                    href: "/docs/build-a-level",
                },
                NavLink {
                    title: "Replace a Blender Material",
                    href: "/docs/replace-a-blender-material",
                },
                NavLink {
                    title: "Sync Cube Size to Avian Collider",
                    href: "/docs/sync-cube-size-to-avian-collider",
                },
            ],
        },
    ];

    Generator::new()
        .insert_resource(NavigationItems(navigation))
        .insert_resource(SiteName(
            "Bevy + Blender = 💕".to_owned(),
        ))
        .add_custom_markdown_directory::<DocFrontMatter>(
            "docs",
        )
        .add_markdown_directory::<PostFrontMatter>("blog")
        .add_ron_directory::<PersonData>("people")
        .add_plugins(ConvertMarkdownToHtml)
        .add_plugins(
            cinnog_mod_markdown::ConvertMarkdownToHtml,
        )
        .build(shell)
        .await
}

#[derive(serde::Deserialize)]
struct PersonData {
    name: String,
    age: u8,
}

impl Ingest for PersonData {
    fn ingest(self, commands: &mut EntityCommands) {
        commands
            .insert((PersonName(self.name), Age(self.age)));
    }
}

#[derive(serde::Deserialize, Default)]
#[serde(default)]
pub struct PostFrontMatter {
    pub href: String,
    pub title: String,
    pub draft: bool,
}

impl Ingest for PostFrontMatter {
    fn ingest(self, commands: &mut EntityCommands) {
        commands.insert((
            // blog_post::TestFontMatter(self.test),
            blog_post::PostTitle(self.title),
        ));
        if self.draft {
            commands.insert(blog_post::DraftPost);
        }
    }

    fn ingest_path(
        &self,
        commands: &mut EntityCommands,
        path: &Path,
    ) {
        commands.insert(blog_post::Post(
            path.file_stem()
                .expect("Path requires file name")
                .to_string_lossy()
                .to_string(),
        ));

        commands.insert(default_bundle_from_path(path));
    }
}

#[derive(serde::Deserialize, Default)]
#[serde(default)]
pub struct DocFrontMatter {
    pub href: String,
    pub title: String,
    pub draft: bool,
}

impl Ingest for DocFrontMatter {
    fn ingest(self, commands: &mut EntityCommands) {
        commands.insert((
            // doc_post::TestFontMatter(self.test),
            doc_post::PostTitle(self.title),
        ));
        if self.draft {
            commands.insert(doc_post::DraftDoc);
        }
    }

    fn ingest_path(
        &self,
        commands: &mut EntityCommands,
        path: &Path,
    ) {
        commands.insert(doc_post::Doc(
            path.file_stem()
                .expect("Path requires file name")
                .to_string_lossy()
                .to_string(),
        ));

        commands.insert(default_bundle_from_path(path));
    }
}
