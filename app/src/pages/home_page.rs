use crate::{
    components::{
        counter::Counter, docs_layout::DocsLayout,
        navigation::Navigation,
    },
    pages::doc_post::{OpengraphImage, PostDescription},
};
use bevy_ecs::{
    component::Component,
    system::{In, Query},
};
use cinnog::run_system_with_input;
use cinnog_mod_markdown::TableOfContents;
use leptos::{component, prelude::*, IntoView};
use leptos_meta::{Link, Meta, Title};
use leptos_router::hooks::use_params_map;

use super::doc_post::{Doc, PostTitle};

#[derive(Component, Clone)]
pub struct PersonName(pub String);

#[derive(Component)]
pub struct Age(pub u8);

#[component]
pub fn HomePage() -> impl IntoView {
    let (
        doc,
        PostTitle(title),
        PostDescription(description),
        OpengraphImage(opengraph_image),
        toc,
    ) = run_system_with_input(
        get_doc,
        "overview".to_string(),
    );
    let title = "Bevy + Blender <3".to_string();
    view! {

        <Title text=title.clone() />
        <Meta
            name="description"
            content=description.clone()
        />

        <Meta property="og:type" content="article"/>
        <Meta
            property="og:url"
            content=format!("https://bevy-skein.netlify.app/")
        />
        <Link
            rel="canonical"
            href=format!("https://bevy-skein.netlify.app/")
        />
        <Meta property="og:image" content=format!("https://bevy-skein.netlify.app{}", opengraph_image.clone()) />
        <Meta name="twitter:card" content="summary_large_image" />
        <Meta name="twitter:creator" content="@chrisbiscardi" />
        <Meta name="twitter:title" content=title.clone() />
        <Meta
            name="twitter:description"
            content=description
        />
        <Meta property="twitter:image" content=format!("https://bevy-skein.netlify.app{}", opengraph_image.clone()) />

        <DocsLayout
            title=title
            table_of_contents=toc
        >
            <div inner_html=doc></div>
        </DocsLayout>
    }
}

fn get_doc(
    In(doc): In<String>,
    docs: Query<(
        &cinnog_mod_markdown::Html,
        &Doc,
        &PostTitle,
        &PostDescription,
        &OpengraphImage,
        &TableOfContents,
    )>,
) -> (
    String,
    PostTitle,
    PostDescription,
    OpengraphImage,
    TableOfContents,
) {
    let (
        cinnog_mod_markdown::Html(html),
        _,
        title,
        description,
        opengraph_image,
        toc,
    ) = &docs
        .iter()
        .find(|(_, file_name, _, _, _, _)| {
            file_name.0 == doc
        })
        .unwrap();
    (
        html.clone(),
        (*title).clone(),
        (*description).clone(),
        (*opengraph_image).clone(),
        (**toc).clone(),
    )
}
