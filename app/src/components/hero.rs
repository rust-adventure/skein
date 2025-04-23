use bevy_ecs::system::Query;
use cinnog::run_system;
use leptos::prelude::*;

use crate::components::button::{Button, ButtonVariant};

#[component]
fn TrafficLightsIcon(class: String) -> impl IntoView {
    view! {
      <svg aria-hidden="true" viewBox="0 0 42 10" fill="none" class=class>
        <circle cx="5" cy="5" r="4.5" />
        <circle cx="21" cy="5" r="4.5" />
        <circle cx="37" cy="5" r="4.5" />
      </svg>
    }
}

#[component]
pub fn Hero() -> impl IntoView {
    let manifest = run_system(get_latest_manifest);

    view! {
      <div class="overflow-hidden bg-slate-900 dark:mt-[-4.75rem] dark:-mb-32 dark:pt-[4.75rem] dark:pb-32 remove-on-dark hero-gradient">
        <div class="py-16 sm:px-2 lg:relative lg:px-0 lg:py-20">
          <div class="mx-auto grid max-w-2xl grid-cols-1 items-center gap-x-8 gap-y-16 px-4 lg:max-w-8xl lg:grid-cols-2 lg:px-8 xl:gap-x-16 xl:px-12">
            <div class="relative z-10 md:text-center lg:text-left">
              <div class="relative">
                <p class="inline bg-linear-to-r from-slate-400 via-[#e27204] to-red-400 bg-clip-text font-display text-5xl tracking-tight text-transparent font-black">
                  "Bevy + Blender <3"
                </p>
                <p class="mt-3 text-2xl tracking-tight text-slate-400">
                    Work with your Bevy Components in Blender and drive Component values using Blender data
                </p>
                <div class="mt-8 flex gap-4 md:justify-center lg:justify-start">
                  <Button href="/">Get started</Button>
                  <Button href="https://github.com/rust-adventure/skein" variant=ButtonVariant::Secondary>
                    View on GitHub
                  </Button>
                  </div>
                  <div class="mt-8 flex gap-4 md:justify-center lg:justify-start">
                  {
                    manifest.map(|manifest| view!{
                      <a
                      href=manifest.release_install_url()
                      class="flex transition bg-white/4 hover:bg-sky-400/7 p-6 sm:p-10 rounded  ring-1 ring-sky-400 ring-inset"
                      >
                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="var(--color-sky-400)" class="size-16 pr-6">
                        <path fill-rule="evenodd" d="M19.5 21a3 3 0 0 0 3-3V9a3 3 0 0 0-3-3h-5.379a.75.75 0 0 1-.53-.22L11.47 3.66A2.25 2.25 0 0 0 9.879 3H4.5a3 3 0 0 0-3 3v12a3 3 0 0 0 3 3h15Zm-6.75-10.5a.75.75 0 0 0-1.5 0v4.19l-1.72-1.72a.75.75 0 0 0-1.06 1.06l3 3a.75.75 0 0 0 1.06 0l3-3a.75.75 0 1 0-1.06-1.06l-1.72 1.72V10.5Z" clip-rule="evenodd" />
                      </svg>
                      <div class="flex flex-col justify-center">
                      <span class="font-black text-slate-400 text-center">"Drag this onto Blender"</span>
                      <span class="font-black text-sky-400 text-center">"v"{manifest.version.clone()}</span>
                      </div>
                      </a>
                    })
                  }
                  </div>
              </div>
            </div>
            <div class="relative">
                <div class="absolute inset-0 rounded bg-linear-to-tr from-sky-300 via-sky-300/70 to-blue-300 opacity-10 blur-lg" />
                <div class="absolute inset-0 rounded bg-linear-to-tr from-sky-300 via-sky-300/70 to-blue-300 opacity-10" />
                <div class="relative rounded bg-[#0A101F]/80 ring-1 ring-white/10 backdrop-blur-sm">
                    <div class="absolute -top-px right-11 left-20 h-px bg-linear-to-r from-sky-300/0 via-sky-300/70 to-sky-300/0" />
                    <div class="absolute right-20 -bottom-px left-11 h-px bg-linear-to-r from-blue-400/0 via-blue-400 to-blue-400/0" />

                    <img
                        class="rounded"
                        src="/hero-blender-components.avif"
                    />
                </div>
            </div>
          </div>
        </div>
      </div>
    }
}

fn get_latest_manifest(
    query: Query<
        &cinnog_mod_blender_addon::BlenderManifest,
    >,
) -> Option<cinnog_mod_blender_addon::BlenderManifestUi> {
    query
        .iter()
        .max_by_key(|m| &m.version)
        .map(|manifest| manifest.to_ui_repr())
}
