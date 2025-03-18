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

#[component]
pub fn Navigation(
    #[prop(default = "".to_string())] class: String,
    // onLinkClick
) -> impl IntoView {
    //   let pathname = usePathname()
    let navigation = expect_resource::<NavigationItems>().0;

    view! {
    <nav class={format!("text-base lg:text-sm {}", class)}>
      <ul role="list" class="space-y-9">
        {navigation.iter().map(|section| view!{
          <li>
            <h2 class="font-display font-medium text-slate-900 dark:text-white">
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
                      // TODO:
                    //   link.href == pathname
                    //     ? "font-semibold text-sky-500 before:bg-sky-500"
                         "text-slate-500 before:hidden before:bg-slate-300 hover:text-slate-600 hover:before:block dark:text-slate-400 dark:before:bg-slate-700 dark:hover:text-slate-300"
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
