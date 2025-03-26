use crate::components::{
    docs_layout::DocsLayout, navigation::Navigation,
};
use bevy_ecs::{
    component::Component,
    prelude::{In, Query},
};
use cinnog::run_system_with_input;
use cinnog_mod_markdown::TableOfContents;
use leptos::prelude::*;
use leptos_meta::{Link, Meta, Title};
use leptos_router::hooks::use_params_map;

#[derive(Component, Clone)]
pub struct TestFontMatter(pub String);

#[derive(Component, Clone)]
pub struct PostTitle(pub String);

#[derive(Component, Clone)]
pub struct PostDescription(pub String);

#[derive(Component, Clone)]
pub struct OpengraphImage(pub String);

#[derive(Component, Clone)]
pub struct DraftDoc;

#[derive(Component, Clone, Default, Debug)]
pub struct Doc(pub String);

#[component]
pub fn DocPost() -> impl IntoView {
    let params = use_params_map().get();
    let current_doc = params.get("doc").unwrap();
    let (
        doc,
        PostTitle(title),
        PostDescription(description),
        OpengraphImage(opengraph_image),
        toc,
    ) = run_system_with_input(get_doc, current_doc.clone());
    view! {

      <Title text=title.clone() />
      <Meta
          name="description"
          content=description.clone()
      />

      <Meta property="og:type" content="article"/>
      <Meta
          property="og:url"
          content=format!("https://bevy-skein.netlify.app/docs/{}", current_doc)
      />
      <Link
          rel="canonical"
          href=format!("https://bevy-skein.netlify.app/docs/{}", current_doc)
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
