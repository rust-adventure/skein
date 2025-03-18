use leptos::{either::Either, prelude::*};
use std::collections::HashMap;

#[derive(Eq, Hash, PartialEq, Default)]
pub enum ButtonVariant {
    #[default]
    Primary,
    Secondary,
}

#[component]
pub fn Button(
    #[prop(optional)] variant: ButtonVariant,
    #[prop(default="".to_string())] class: String,
    #[prop(optional)] href: Option<&'static str>,
    children: Children,
) -> impl IntoView {
    let variants = HashMap::from([(
        ButtonVariant::Primary,
          "rounded-full bg-sky-300 py-2 px-4 text-sm font-semibold text-slate-900 hover:bg-sky-200 focus:outline-hidden focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-300/50 active:bg-sky-500"
        ),
        (
          ButtonVariant::Secondary,
          "rounded-full bg-slate-800 py-2 px-4 text-sm font-medium text-white hover:bg-slate-700 focus:outline-hidden focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white/50 active:text-slate-400"
        ),
      ]);
    let classes = format!(
        "{} {}",
        variants.get(&variant).unwrap(),
        class
    );

    match href {
        Some(href) => Either::Left(
            view! {<a href=href class=classes>{children()}</a>},
        ),
        None => Either::Right(
            view! {<button class=classes>{children()}</button>},
        ),
    }
}
