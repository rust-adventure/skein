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
