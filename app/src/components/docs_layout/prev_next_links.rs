use crate::NavigationItems;
use cinnog::expect_resource;
use leptos::prelude::*;

#[component]
fn ArrowIcon(class: String) -> impl IntoView {
    view! {
      <svg viewBox="0 0 16 16" aria-hidden="true" class=class>
        <path d="m9.182 13.423-1.17-1.16 3.505-3.505H3V7.065h8.517l-3.506-3.5L9.181 2.4l5.512 5.511-5.511 5.512Z" />
      </svg>
    }
}

#[derive(PartialEq)]
enum PageDirection {
    Previous,
    Next,
}
impl PageDirection {
    fn label(&self) -> &'static str {
        match self {
            PageDirection::Previous => "Previous",
            PageDirection::Next => "Next",
        }
    }
}
#[component]
fn PageLink(
    title: String,
    href: String,
    #[prop(default=PageDirection::Next)] dir: PageDirection,
) -> impl IntoView {
    view! {
    <div>
      <dt class="font-display text-sm font-medium text-slate-900 dark:text-white">
        {dir.label()}
      </dt>
      <dd class="mt-1">
        <a
          href={href}
          class={format!(
            "flex items-center gap-x-1 text-base font-semibold text-slate-500 hover:text-slate-600 dark:text-slate-400 dark:hover:text-slate-300 {}",
            if dir == PageDirection::Previous {
                 "flex-row-reverse"
            }else {
                ""
            }
          )}
        >
          {title}
          <ArrowIcon
            class={format!(
              "h-4 w-4 flex-none fill-current {}",
              if dir == PageDirection::Previous {
                "-scale-x-100"
              } else {
                ""
              }
            )}
          />
        </a>
      </dd>
    </div>
    }
}

#[component]
pub fn PrevNextLinks() -> impl IntoView {
    let navigation = expect_resource::<NavigationItems>().0;
    let url = leptos_router::hooks::use_url();

    let section = navigation
        .iter()
        .flat_map(|category| &category.links)
        .find(|link| link.href == url.get().path());

    section.map(|current_page| {

        let mut it = navigation
            .iter()
            .flat_map(|category| category.links.iter());

        let position = it.clone().position(|nav_link| nav_link.href == current_page.href);

        let previous_page = position.and_then(|pos| it.clone().nth(pos.wrapping_sub(1)));
        let next_page = position.and_then(|pos| it.clone().nth(pos + 1));

        view! {
            <dl class="mt-12 flex border-t border-slate-200 pt-6 dark:border-slate-800">
            {previous_page.map(|page| view! {
                <PageLink
                    dir=PageDirection::Previous
                    title={page.title.to_string()}
                    href={page.href.to_string()}
                />
            })}
            {next_page.map(|page| view! {
                <PageLink
                    title={page.title.to_string()}
                    href={page.href.to_string()}
                    {..}
                    class="ml-auto text-right"
                />
            })}
            </dl>
        }.into_any()
    })
}
