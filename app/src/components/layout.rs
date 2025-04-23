use cinnog::run_system;
use leptos::prelude::*;

use crate::components::{
    hero::Hero, mobile_navigation::MobileNavigation,
    navigation::Navigation,
};

#[component]
fn GitHubIcon(class: String) -> impl IntoView {
    view! {
      <svg aria-hidden="true" viewBox="0 0 16 16" class=class>
        <path d="M8 0C3.58 0 0 3.58 0 8C0 11.54 2.29 14.53 5.47 15.59C5.87 15.66 6.02 15.42 6.02 15.21C6.02 15.02 6.01 14.39 6.01 13.72C4 14.09 3.48 13.23 3.32 12.78C3.23 12.55 2.84 11.84 2.5 11.65C2.22 11.5 1.82 11.13 2.49 11.12C3.12 11.11 3.57 11.7 3.72 11.94C4.44 13.15 5.59 12.81 6.05 12.6C6.12 12.08 6.33 11.73 6.56 11.53C4.78 11.33 2.92 10.64 2.92 7.58C2.92 6.71 3.23 5.99 3.74 5.43C3.66 5.23 3.38 4.41 3.82 3.31C3.82 3.31 4.49 3.1 6.02 4.13C6.66 3.95 7.34 3.86 8.02 3.86C8.7 3.86 9.38 3.95 10.02 4.13C11.55 3.09 12.22 3.31 12.22 3.31C12.66 4.41 12.38 5.23 12.3 5.43C12.81 5.99 13.12 6.7 13.12 7.58C13.12 10.65 11.25 11.33 9.47 11.53C9.76 11.78 10.01 12.26 10.01 13.01C10.01 14.08 10 14.94 10 15.21C10 15.42 10.15 15.67 10.55 15.59C13.71 14.53 16 11.53 16 8C16 3.58 12.42 0 8 0Z" />
      </svg>
    }
}

#[component]
fn Logo(class: String) -> impl IntoView {
    view! {
        <svg
        class=class
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 277.97 82.94"><path d="M31.13 82.94c-6.67 0-12.48-.97-17.44-2.92S4.17 74.98 0 70.73l13.75-13.75c2.86 2.71 5.87 4.79 9.02 6.22 3.15 1.43 6.53 2.14 10.12 2.14 3.01 0 5.28-.46 6.82-1.38 1.54-.92 2.31-2.18 2.31-3.79s-.66-2.95-1.98-4.02c-1.32-1.06-3.06-2.02-5.23-2.86-2.16-.84-4.55-1.7-7.15-2.58-2.6-.88-5.19-1.94-7.76-3.19a35.168 35.168 0 0 1-7.09-4.56c-2.16-1.8-3.91-4.03-5.23-6.71-1.32-2.68-1.98-5.96-1.98-9.85 0-5.06 1.21-9.42 3.63-13.09s5.83-6.47 10.23-8.42c4.4-1.94 9.57-2.92 15.51-2.92s11.31.94 16.33 2.81c5.02 1.87 9.19 4.53 12.48 7.98L49.92 26.51c-2.42-2.35-4.84-4.09-7.26-5.23-2.42-1.14-5.06-1.71-7.92-1.71-2.27 0-4.09.37-5.44 1.1-1.36.73-2.04 1.83-2.04 3.3 0 1.54.66 2.81 1.98 3.79 1.32.99 3.06 1.89 5.23 2.7 2.16.81 4.55 1.65 7.15 2.53 2.6.88 5.19 1.93 7.75 3.14 2.57 1.21 4.93 2.75 7.1 4.62 2.16 1.87 3.9 4.2 5.23 6.99 1.32 2.79 1.98 6.16 1.98 10.12 0 7.99-2.84 14.17-8.52 18.54-5.68 4.36-13.7 6.54-24.04 6.54ZM71.5 81.62V1.1h21.56v80.52H71.5Zm34.87 0L91.3 53.13l14.96-25.63h23.21l-19.36 28.93.55-7.04 19.91 32.23h-24.2Z"/><path d="M162.03 82.94c-6.23 0-11.77-1.23-16.61-3.69s-8.65-5.83-11.44-10.12c-2.79-4.29-4.18-9.19-4.18-14.69s1.32-10.27 3.96-14.52c2.64-4.25 6.27-7.61 10.89-10.06 4.62-2.46 9.86-3.69 15.73-3.69 6.38 0 11.79 1.48 16.22 4.46 4.44 2.97 7.68 7.28 9.74 12.92l-34.21 32.01-10.12-10.45 30.91-28.82-2.2 13.42c-.66-2.57-1.87-4.51-3.63-5.83-1.76-1.32-4-1.98-6.71-1.98-2.35 0-4.36.46-6.05 1.38-1.69.92-2.97 2.24-3.85 3.96-.88 1.72-1.32 3.79-1.32 6.21 0 2.86.61 5.39 1.82 7.59s2.9 3.92 5.06 5.17c2.16 1.25 4.6 1.87 7.32 1.87 2.27 0 4.31-.42 6.1-1.27 1.8-.84 3.61-2.25 5.45-4.23l10.78 10.67c-3.15 3.3-6.67 5.74-10.56 7.31-3.89 1.58-8.25 2.37-13.09 2.37ZM203.06 22.44c-3.15 0-5.77-1.08-7.87-3.24-2.09-2.16-3.13-4.82-3.13-7.98s1.04-5.81 3.13-7.98c2.09-2.16 4.71-3.25 7.87-3.25s5.87 1.08 7.92 3.25c2.05 2.16 3.08 4.82 3.08 7.98s-1.03 5.81-3.08 7.98c-2.05 2.16-4.69 3.24-7.92 3.24Zm-10.78 59.18V27.5h21.56v54.12h-21.56ZM222.64 81.62V51.7c0-5.13 1.17-9.61 3.52-13.42 2.35-3.81 5.61-6.78 9.79-8.91 4.18-2.13 8.98-3.19 14.41-3.19s10.32 1.06 14.46 3.19c4.14 2.13 7.37 5.1 9.68 8.91 2.31 3.81 3.46 8.29 3.46 13.42v29.92H256.4V51.48c0-2.27-.55-4.01-1.65-5.23-1.1-1.21-2.57-1.81-4.4-1.81s-3.41.6-4.51 1.81c-1.1 1.21-1.65 2.95-1.65 5.23v30.14h-21.56Z"/></svg>
    }
}
#[component]
fn Header() -> impl IntoView {
    let is_scrolled = true;
    view! {
    <header
      class=format!(
        "sticky top-0 z-50 flex flex-none flex-wrap items-center justify-between bg-white px-4 py-5 shadow-md shadow-slate-900/5 transition duration-500 sm:px-6 lg:px-8 dark:shadow-none {}",
        if is_scrolled {
           "dark:bg-slate-900/95 dark:backdrop-blur-sm dark:[@supports(backdrop-filter:blur(0))]:bg-slate-900/75"
        }
          else {"dark:bg-transparent"},
      )
    >
      <div class="mr-6 flex lg:hidden">
        <MobileNavigation />
      </div>
      <div class="relative flex grow basis-0 items-center">
        <a href="/" aria-label="Home page">
        //   <Logomark class="h-9 w-9 lg:hidden" />
          <Logo class="hidden h-9 w-auto fill-slate-700 lg:block dark:fill-sky-100".to_string() />
        </a>
      </div>
      <div class="-my-5 mr-6 sm:mr-8 md:mr-0">
        // <Search />
      </div>
      <div class="relative flex basis-0 justify-end gap-6 sm:gap-8 md:grow">
        <a href="https://github.com/rust-adventure/skein" class="group" aria-label="GitHub">
          <GitHubIcon class="h-6 w-6 fill-slate-400 group-hover:fill-slate-500 dark:group-hover:fill-slate-300".to_string() />
        </a>
      </div>
    </header>
    }
}

#[component]
pub fn Layout(children: Children) -> impl IntoView {
    let url = leptos_router::hooks::use_url();

    view! {
      <div class="flex w-full flex-col">
        <div class="remove-on-light hero-gradient oversized-hero-gradient"/>
        <Header />

        {(url.get().path() == "/").then_some(view!{<Hero />})}


        <div class="relative mx-auto flex w-full max-w-8xl flex-auto justify-center sm:px-2 lg:px-8 xl:px-12">
          <div class="hidden lg:relative lg:block lg:flex-none">
            <div class="absolute inset-y-0 right-0 w-[50vw] bg-slate-50 dark:hidden" />
            <div class="absolute top-16 right-0 bottom-0 hidden h-12 w-px bg-linear-to-t from-slate-800 dark:block" />
            <div class="absolute top-28 right-0 bottom-0 hidden w-px bg-slate-800 dark:block" />
            <div class="sticky top-[4.75rem] -ml-0.5 h-[calc(100vh-4.75rem)] w-64 overflow-x-hidden overflow-y-auto py-16 pr-8 pl-0.5 xl:w-72 xl:pr-16">
              <Navigation />
            </div>
          </div>
          {children()}
        </div>
      </div>
    }
}
