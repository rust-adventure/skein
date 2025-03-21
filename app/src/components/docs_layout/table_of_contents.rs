use std::collections::HashMap;

use cinnog_mod_markdown::TocNode;
use leptos::{logging::log, prelude::*};
use leptos_use::{
    use_scroll_with_options, use_window, use_window_scroll,
    ScrollOffset, UseScrollOptions, UseScrollReturn,
};

struct ToCItem {
    id: String,
}

const COLORS: [&str; 17] = [
    "text-indigo-400",
    "text-violet-400",
    "text-purple-400",
    "text-fuchsia-400",
    "text-pink-400",
    "text-rose-400",
    "text-red-400",
    "text-orange-400",
    "text-amber-400",
    "text-yellow-400",
    "text-lime-400",
    "text-green-400",
    "text-emerald-400",
    "text-teal-400",
    "text-cyan-400",
    "text-sky-400",
    "text-blue-400",
];

fn is_active(section: &TocNode, current: String) -> bool {
    if section.id == current {
        return true;
    }
    if section.items.is_empty() {
        return false;
    }
    section
        .items
        .iter()
        .find(|node| node.id == current)
        .is_some()
}

#[island]
pub fn TableOfContents(
    table_of_contents: cinnog_mod_markdown::TableOfContents,
) -> impl IntoView {
    #[cfg(not(feature = "ssr"))]
    let (x, y) = use_window_scroll();
    let mut map: HashMap<String, TocNode> =
        HashMap::default();
    let heading_ids = table_of_contents
        .items
        .clone()
        .into_iter()
        .flat_map(|node| {
            map.insert(node.id.clone(), node.clone());
            let mut v = vec![node.id.clone()];
            for item in node.items.iter() {
                map.insert(item.id.clone(), item.clone());
                v.push(item.id.clone());
            }
            v
        })
        .collect::<Vec<_>>();

    let (current_section, set_current_section) = signal(
        table_of_contents
            .items
            .get(0)
            .map(|node| node.clone())
            .unwrap_or(TocNode {
                text: "".to_string(),
                id: "".to_string(),
                items: vec![],
            }),
    );

    #[cfg(not(feature = "ssr"))]
    Effect::new(move |_| {
        if heading_ids.is_empty() {
            return;
        }
        let mut positions = vec![];
        let doc = window().document().unwrap();

        for id in heading_ids.iter() {
            log!("heading {}", id);
            let Some(el) = doc.get_element_by_id(id) else {
                continue;
            };
            let Ok(Some(style)) =
                window().get_computed_style(&el)
            else {
                continue;
            };
            let Ok(scroll_margin_top_str) = style
                .get_property_value("scroll-margin-top")
            else {
                continue;
            };
            let Ok(scroll_margin_top) =
                scroll_margin_top_str
                    .trim_end_matches("px")
                    .parse::<f64>()
            else {
                continue;
            };

            let top = y()
                + el.get_bounding_client_rect().top()
                - scroll_margin_top;
            positions.push((id, top));
        }
        let mut current = &heading_ids[0];

        for heading in positions.iter() {
            if y() >= (heading.1 - 10.) {
                current = heading.0
            } else {
                break;
            }
        }

        let Some(new_current) = map.get(current) else {
            return;
        };
        set_current_section((*new_current).clone())
    });

    view! {
      <div class="hidden xl:sticky xl:top-[4.75rem] xl:-mr-6 xl:block xl:h-[calc(100vh-4.75rem)] xl:flex-none xl:overflow-y-auto xl:py-16 xl:pr-6">
        <nav aria-labelledby="on-this-page-title" class="w-56">
          {(!table_of_contents.items.is_empty()).then_some(view!{
              <h2
                id="on-this-page-title"
                class="font-display text-sm font-medium text-slate-900 dark:text-white"
              >
                On this page
              </h2>
              <ol role="list" class="mt-4 space-y-3 text-sm">
                {table_of_contents.items.clone()
                    .into_iter()
                    .enumerate()
                    .map(|(i, section)|{
                      let section_clone = section.clone();
                  view!{
                  <li>
                    <h3>
                      <a
                        href={format!("#{}", section.id)}
                        class={
                          move || if is_active(&section_clone, current_section().id) {
                            "text-sky-500"
                          } else {
                            "font-normal text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-300"
                          }
                        }
                      >
                        {section.text.clone()}
                      </a>
                    </h3>
                    {(!section.items.is_empty()).then_some(
                      view!{
                        <ol
                        role="list"
                        class="mt-2 space-y-3 pl-5 text-slate-500 dark:text-slate-400"
                      >
                        {section.items.clone().into_iter().map(|sub_section| {
                          let href = format!("#{}", &sub_section.id);
                          view!{
                          <li>
                            <a
                            href={href}
                              class={
                              move  || if is_active(&sub_section, current_section().id) {
                                   "text-sky-500"
                               }else {
                                  "hover:text-slate-600 dark:hover:text-slate-300"
                               }
                              }
                            >
                              {sub_section.text.clone()}
                            </a>
                          </li>
                        }
                      }).collect_view()}
                      </ol>
                      })
                    }

                  </li>
                  }
                }).collect_view()}
              </ol>
            }
          )}
        </nav>
      </div>
    }
}
