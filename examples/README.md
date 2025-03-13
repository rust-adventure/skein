# Examples

replace

Example | Description
--- | ---
[component_tests](../examples/component_tests.rs) | Sets up a series of components that cover a variety of use cases. Useful for testing that UI in Blender is rendered appropriately. Also used in `lib.rs`'s tests.
[debug](../examples/debug.rs) | a "hello world" level example that uses a small .gltf file to show how glTF data translates into components
[event_ordering](../examples/event_ordering.rs) | Shows the order in which `SceneInstanceReady` and `SkeinSceneInstanceReady` happen, and when components are accessible
[replace_material](../examples/replace_material.rs) | Place a Component on a Material in Blender, and replace that material in Bevy using a Component on_add Hook.