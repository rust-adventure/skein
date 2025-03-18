use cinnog::expect_resource;
// import { DocsHeader } from
// '@/components/DocsHeader'
// import { PrevNextLinks } from
// '@/components/PrevNextLinks' import { Prose }
// from '@/components/Prose'
// import { TableOfContents } from
// '@/components/TableOfContents'
// import { collectSections } from
// '@/lib/sections'
use leptos::{either::EitherOf4, prelude::*};
use table_of_contents::TableOfContents;
mod table_of_contents;

use crate::{
    components::prose::Prose, NavLink, NavigationItems,
};

#[component]
pub fn DocsLayout(
    children: Children,
    title: String,
) -> impl IntoView {
    // nodes
    //   let tableOfContents = collectSections(nodes)

    view! {

        <div class="max-w-2xl min-w-0 flex-auto px-4 py-16 lg:max-w-none lg:pr-0 lg:pl-8 xl:px-16">
          <article>
            <DocsHeader title={title} />
            <Prose>{children()}</Prose>
          </article>
          // <PrevNextLinks />
        </div>
        <TableOfContents table_of_contents={vec![]} />

    }
}

// import { usePathname } from 'next/navigation'
// import { navigation } from '@/lib/navigation'

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

    // if title.is_none() && section.is_none() {
    //     return view! {};
    // }

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
