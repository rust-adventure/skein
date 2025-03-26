#![allow(clippy::type_complexity)]
mod components;
pub mod pages;

use components::layout::Layout;
pub use components::navigation::{
    NavItem, NavLink, NavigationItems,
};
use pages::{
    blog::Blog,
    doc_post::{Doc, DocPost},
    home_page::HomePage,
    not_found::NotFound,
};

use crate::pages::blog_post::BlogPost;
use bevy_ecs::{
    prelude::Resource, query::With, system::Query,
};
use cinnog::{run_system, FileName};
use leptos::{prelude::*, IntoView};
use leptos_meta::*;
use leptos_router::{
    components::*, path, static_routes::StaticRoute,
    SsrMode,
};
use pages::blog_post::Post;

pub fn shell(options: LeptosOptions) -> impl IntoView {
    view! {
        <!DOCTYPE html>
        <html lang="en" class="h-full antialiased">
            <head>
                <meta charset="utf-8"/>
                <meta name="viewport" content="width=device-width, initial-scale=1"/>
                <AutoReload options=options.clone()/>
                <HydrationScripts options islands=true/>
                <MetaTags/>
            </head>
            <body class="flex min-h-full bg-white dark:bg-slate-900">
                <App/>
            </body>
        </html>
    }
}

#[component]
pub fn App() -> impl IntoView {
    provide_meta_context();
    let fallback =
        || view! { "Page not found." }.into_view();

    view! {
        <Stylesheet href="/pkg/cinnog_example.css"/>
        <Title text="Skein: Bevy and Blender"/>

        <Router>
        <Layout>
                <FlatRoutes fallback>
                    <Route
                        path=path!("/")
                        view=HomePage
                        ssr=SsrMode::Static(
                            StaticRoute::new(),
                        )
                    />

                    <Route
                        path=path!("/404")
                        view=NotFound
                        ssr=SsrMode::Static(
                            StaticRoute::new(),
                        )
                    />

                    <Route
                        path=path!("/blog")
                        view=Blog
                        ssr=SsrMode::Static(
                            StaticRoute::new(),
                        )
                    />

                    <Route
                        path=path!("/blog/*post")
                        view=BlogPost
                        ssr=SsrMode::Static(
                            StaticRoute::new()
                                .prerender_params(|| async move {
                                    [("post".into(), run_system(blog_static_params))]
                                        .into_iter()
                                        .collect()
                                }),
                        )
                    />

                    <Route
                        path=path!("/docs/*doc")
                        view=DocPost
                        ssr=SsrMode::Static(
                            StaticRoute::new()
                                .prerender_params(|| async move {
                                    [("doc".into(), run_system(docs_static_params))]
                                        .into_iter()
                                        .collect()
                                }),
                        )
                    />
                </FlatRoutes>
            </Layout>
        </Router>
    }
}

fn blog_static_params(
    posts: Query<&FileName, With<Post>>,
) -> Vec<String> {
    posts.iter().map(|post| post.0.clone()).collect()
}

fn docs_static_params(
    docs: Query<&FileName, With<Doc>>,
) -> Vec<String> {
    docs.iter().map(|doc| doc.0.clone()).collect()
}

#[derive(Resource, Clone)]
pub struct SiteName(pub String);
