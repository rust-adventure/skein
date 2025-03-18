use crate::pages::home_page::PersonName;
use crate::SiteName;
use bevy_ecs::system::Query;
use cinnog::{expect_resource, run_system, FileName};
use leptos::prelude::*;

#[component]
pub fn Navigation() -> impl IntoView {
    let site_name = expect_resource::<SiteName>().0;
    let persons = run_system(get_people);
    view! {
        <div class="nav">
            <a href="/">{site_name}</a>
            <ul class="people-links">
                <li>
                    <a href="/blog.html">Blog</a>
                </li>
                {persons
                    .into_iter()
                    .map(|(id, person)| {
                        view! {
                            <li>
                                <a href=format!("/person/{}", id.0)>{person.0}</a>
                            </li>
                        }
                    })
                    .collect::<Vec<_>>()}
            </ul>
        </div>
    }
}

fn get_people(people: Query<(&FileName, &PersonName)>) -> Vec<(FileName, PersonName)> {
    people
        .iter()
        .map(|(id, person)| (id.clone(), person.clone()))
        .collect()
}
