/// List all of the Components in a regular Bevy
/// application
use bevy::prelude::*;
use std::any::TypeId;
use std::fs::File;
use std::io::Write;

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .add_systems(Startup, startup)
        .run();
}

fn startup(type_registry: Res<AppTypeRegistry>,        mut app_exit_events: EventWriter<AppExit>,
) -> Result {
    let types = type_registry.read();
    let mut component_types: Vec<_> = vec![];
    for registration in types.iter() {
        //    (TypeId::of::<ReflectComponent>(), "Component")
        //    (TypeId::of::<ReflectResource>(), "Resource")
        //    (TypeId::of::<ReflectDefault>(), "Default")
        //    (TypeId::of::<ReflectSerialize>(), "Serialize")
        //    (TypeId::of::<ReflectDeserialize>(), "Deserialize")
        let id = TypeId::of::<ReflectComponent>();
        if registration.data_by_id(id).is_some() {
            let binding = registration.type_info().type_path_table();

            let short_path = binding.short_path();
            let type_path = binding.path();
            component_types.push(type_path);
        }
    }
    component_types.sort();
   
    let mut f = File::create_new("types.json")?;
    f.write_all(serde_json::to_string_pretty(&component_types).unwrap().as_bytes())?;
    
    info!("file");
    app_exit_events.write(AppExit::Success);
    Ok(())
}



