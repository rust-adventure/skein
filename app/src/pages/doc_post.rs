use crate::components::{
    docs_layout::DocsLayout, navigation::Navigation,
};
use bevy_ecs::{
    component::Component,
    prelude::{In, Query},
};
use cinnog::run_system_with_input;
use leptos::prelude::*;
use leptos_router::hooks::use_params_map;

#[derive(Component, Clone)]
pub struct TestFontMatter(pub String);

#[derive(Component, Clone)]
pub struct PostTitle(pub String);

#[derive(Component, Clone)]
pub struct DraftDoc;

#[derive(Component, Clone, Default, Debug)]
pub struct Doc(pub String);

#[component]
pub fn DocPost() -> impl IntoView {
    let params = use_params_map().get();
    let current_doc = params.get("doc").unwrap();
    let (doc, title) =
        run_system_with_input(get_doc, current_doc.clone());
    view! {
        <DocsLayout title=title>
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
        .find(|(_, file_name, _)| file_name.0 == doc)
        .unwrap();
    (html.clone(), title.0.clone())
}
