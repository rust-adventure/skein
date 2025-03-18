use crate::components::{
    counter::Counter, docs_layout::DocsLayout,
    navigation::Navigation,
};
use bevy_ecs::{
    component::Component,
    system::{In, Query},
};
use cinnog::run_system_with_input;
use leptos::{component, prelude::*, IntoView};
use leptos_router::hooks::use_params_map;

use super::doc_post::{Doc, PostTitle};

#[derive(Component, Clone)]
pub struct PersonName(pub String);

#[derive(Component)]
pub struct Age(pub u8);

#[component]
pub fn HomePage() -> impl IntoView {
    let (doc, title) = run_system_with_input(
        get_doc,
        "getting-started".to_string(),
    );

    view! {
        <DocsLayout title="Getting Started".to_string()>
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
    )>,
) -> (String, String) {
    let (cinnog_mod_markdown::Html(html), _, title) = &docs
        .iter()
        .find(|(_, file_name, _)| {
            file_name.0 == "getting-started"
        })
        .unwrap();
    (html.clone(), title.0.clone())
}
