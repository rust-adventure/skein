use bevy_ecs::system::Query;
use cinnog::{expect_resource, run_system};
use leptos::{either::EitherOf4, prelude::*};
use table_of_contents::TableOfContents;
mod prev_next_links;
mod table_of_contents;

use crate::{
    components::prose::Prose, NavLink, NavigationItems,
};
use prev_next_links::PrevNextLinks;

#[component]
pub fn DocsLayout(
    children: Children,
    title: String,
    #[prop(optional)]
    table_of_contents: cinnog_mod_markdown::TableOfContents,
) -> impl IntoView {
    view! {
        <div class="max-w-2xl min-w-0 flex-auto px-4 py-16 lg:max-w-none lg:pr-0 lg:pl-8 xl:px-16">
          <article>
            <DocsHeader title={title} />
            <Prose>{children()}</Prose>
          </article>
          <PrevNextLinks />
        </div>
        <TableOfContents table_of_contents={table_of_contents} />

    }
}

#[component]
fn DocsHeader(
    #[prop(optional)] title: Option<String>,
) -> impl IntoView {
    let navigation = expect_resource::<NavigationItems>().0;
    let url = leptos_router::hooks::use_url();

    let section = navigation.iter().find(|links| {
        links
            .links
            .iter()
            .find(|link| link.href == url.get().path())
            .is_some()
    });

    view! {
        <header class="mb-9 space-y-1">
          {section.map(|section| view!{
            <p class="font-display text-sm font-medium text-sky-500">
              {section.title}
            </p>
          })}
          {title.map(|title|view!{
            <h1 class="font-display text-3xl tracking-tight text-slate-900 dark:text-white">
              {title}
            </h1>
          })}
        </header>
    }
}
