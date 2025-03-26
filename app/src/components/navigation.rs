use bevy_ecs::system::Resource;
use cinnog::expect_resource;
use leptos::prelude::*;

#[derive(Clone)]
pub struct NavItem {
    pub title: &'static str,
    pub links: Vec<NavLink>,
}
#[derive(Clone)]
pub struct NavLink {
    pub title: &'static str,
    pub href: &'static str,
}

#[derive(Resource, Clone)]
pub struct NavigationItems(pub Vec<NavItem>);

const COLORS: [&str; 9] = [
    "text-indigo-500",
    // "text-violet-500",
    "text-purple-500",
    // "text-fuchsia-500",
    "text-pink-500",
    // "text-rose-500",
    "text-red-500",
    // "text-orange-500",
    "text-amber-500",
    // "text-yellow-500",
    "text-lime-500",
    // "text-green-500",
    "text-emerald-500",
    // "text-teal-500",
    "text-cyan-500",
    // "text-sky-500",
    "text-blue-500",
];

const COLORS_DARK: [&str; 9] = [
    "dark:text-indigo-400",
    // "dark:text-violet-400",
    "dark:text-purple-400",
    // "dark:text-fuchsia-400",
    "dark:text-pink-400",
    // "dark:text-rose-400",
    "dark:text-red-400",
    // "dark:text-orange-400",
    "dark:text-amber-400",
    // "dark:text-yellow-400",
    "dark:text-lime-400",
    // "dark:text-green-400",
    "dark:text-emerald-400",
    // "dark:text-teal-400",
    "dark:text-cyan-400",
    // "dark:text-sky-400",
    "dark:text-blue-400",
];

#[component]
pub fn Navigation(
    #[prop(default = "".to_string())] class: String,
) -> impl IntoView {
    let navigation = expect_resource::<NavigationItems>().0;

    let url = leptos_router::hooks::use_url();

    view! {
    <nav class={format!("text-base lg:text-sm {}", class)}>
      <ul role="list" class="space-y-9">
        {navigation.iter().enumerate().map(|(i, section)| view!{
          <li>
            <h2 class=format!("font-display font-medium {} {}", COLORS[i], COLORS_DARK[i])>
              {section.title}
            </h2>
            <ul
              role="list"
              class="mt-2 space-y-2 border-l-2 border-slate-100 lg:mt-4 lg:space-y-4 lg:border-slate-200 dark:border-slate-800"
            >
              {section.links.iter().map(|link| view!{
                <li class="relative">
                  <a
                    href={link.href}
                    // onClick={onLinkClick}
                    class={format!(
                      "block w-full pl-3.5 before:pointer-events-none before:absolute before:top-1/2 before:-left-1 before:h-1.5 before:w-1.5 before:-translate-y-1/2 before:rounded-full {}",
                      if link.href == url.get().path() {
                         "font-semibold text-sky-500 before:bg-sky-500"
                      } else {
                         "text-slate-500 before:hidden before:bg-slate-300 hover:text-slate-600 hover:before:block dark:text-slate-400 dark:before:bg-slate-700 dark:hover:text-slate-300"
                      }
                    )}
                  >
                    {link.title}
                  </a>
                </li>
              }).collect_view()}
            </ul>
          </li>
        }).collect_view()}
      </ul>
    </nav>
    }
}
