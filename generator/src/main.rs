use app::{
    pages::{blog_post, doc_post},
    shell, NavItem, NavLink, NavigationItems, SiteName,
};
use bevy_ecs::system::EntityCommands;
use cinnog::{
    default_bundle_from_path,
    generator::Generator,
    loaders::markdown::{
        ConvertMarkdownToHtml, MarkdownDataLayer,
    },
    Ingest,
};
use cinnog_mod_blender_addon::BlenderAddonZipDataLayer;
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
                    title: "Overview",
                    href: "/",
                },
                NavLink {
                    title: "Quickstart",
                    href: "/docs/quickstart",
                },
                NavLink {
                    title: "Getting started",
                    href: "/docs/getting-started",
                },
                NavLink {
                    title: "Installation",
                    href: "/docs/installation",
                },
                NavLink {
                    title: "Fetching the Bevy Type Registry",
                    href: "/docs/fetching-the-bevy-type-registry",
                },
                NavLink {
                    title: "Inserting Components",
                    href: "/docs/inserting-components",
                },
                NavLink {
                    title: "Defaults and Presets",
                    href: "/docs/defaults-and-presets",
                },
            ],
        },
        NavItem {
            title: "The Blender Addon",
            links: vec![
                NavLink {
                    title: "Using Blender Drivers",
                    href: "/docs/using-blender-drivers",
                },
                NavLink {
                    title: "Collection Instances and Library Overrides",
                    href: "/docs/collections-instances-and-library-overrides",
                },
            ],
        },
        NavItem {
            title: "Exporting",
            links: vec![
                NavLink {
                    title: "The Basics",
                    href: "/docs/exporting-the-basics"
                },
                NavLink {
                    title: "Multiple Collections",
                    href: "/docs/exporting-multiple-collections"
                },
            ]
        },
        NavItem {
            title: "Concepts",
            links: vec![
                NavLink {
                    title: "Components as APIs",
                    href: "/docs/components-as-apis"
                }
            ]
        },
        NavItem {
            title: "Use Cases",
            links: vec![
                // NavLink {
                //     title: "Build a Level (coming soon)",
                //     href: "/docs/build-a-level",
                // },
                NavLink {
                    title: "Mark and Modify Blender Objects",
                    href: "/docs/mark-and-modify-blender-objects",
                },
                NavLink {
                    title: "Replace a Blender Material",
                    href: "/docs/replace-a-blender-material",
                },
                // NavLink {
                //     title: "Sync Cube Size to Avian Collider (coming soon)",
                //     href: "/docs/sync-cube-size-to-avian-collider",
                // },
                // vleue_navigator pathfinding
                // networking example server/client
                // bevy_hanabi integration (Spawners, etc)
                // light baking examples
            ],
        },
        NavItem {
            title: "Use Cases (Advanced)",
            links: vec![
                NavLink {
                    title: "Using sub-assets",
                    href: "/docs/using-sub-assets",
                },
                NavLink {
                    title: "Exporting Materials to Files",
                    href: "/docs/exporting-materials-to-files",
                },
            ]
        },
        NavItem {
            title: "Experimental",
            links: vec![
                NavLink {
                    title: "Migration Tools",
                    href: "/docs/migration-tools",
                }
            ]
        },
        NavItem {
            title: "Contributing and Internals",
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
                NavLink {
                    title: "Bevy Remote Protocol",
                    href: "/docs/bevy-remote-protocol",
                },
                NavLink {
                    title: "Reflection",
                    href: "/docs/reflection",
                },
            ],
        },
        NavItem {
            title: "FAQ",
            links: vec![
                NavLink {
                    title: "Compared to Blenvy",
                    href: "/docs/compared-to-blenvy",
                },
                NavLink {
                    title: "Compared to Blenvy",
                    href: "/docs/blender",
                },
            ]
        }
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
        .add_blender_addon_zips_directory("assets/releases")
        .add_plugins(ConvertMarkdownToHtml)
        .add_plugins(
            cinnog_mod_markdown::ConvertMarkdownToHtml,
        )
        // .add_plugins
        .build(shell)
        .await
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
    pub description: String,
    pub opengraph_image: String,
    pub draft: bool,
}

impl Ingest for DocFrontMatter {
    fn ingest(self, commands: &mut EntityCommands) {
        commands.insert((
            // doc_post::TestFontMatter(self.test),
            doc_post::OpengraphImage(self.opengraph_image),
            doc_post::PostTitle(self.title),
            doc_post::PostDescription(self.description),
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
