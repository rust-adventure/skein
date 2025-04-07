import inspect
from pathlib import Path
import bpy # type: ignore
import json
import requests # type: ignore
from .property_groups import hash_over_64, make_property
# --------------------------------- #
#  Fetch and store the bevy type    #
#  registry, for panel display      #
# --------------------------------- #

class FetchBevyTypeRegistry(bpy.types.Operator):
    """Fetch the Bevy type registry via the Bevy Remote Protocol"""
    bl_idname = "wm.fetch_type_registry" # unique identifier. not specially named
    bl_label = "Fetch Bevy Type Registry" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    # execute is called to run the operator
    def execute(self, context):
        debug = False
        if __package__ in context.preferences.addons:
            debug = context.preferences.addons[__package__].preferences.debug

        if debug:
            print("\nexecute: FetchBevyTypeRegistry")

        brp_response = None

        try:
            brp_response = brp_fetch_registry_schema()
        except:
            self.report({"ERROR"}, "Could not connect to bevy application to fetch registry data from the Bevy Remote Protocol")
            return {'CANCELLED'}

        # If the bevy remote protocol returns an error, report it to the user
        if brp_response is not None and "error" in brp_response:
            if debug:
                print("bevy request errored out", brp_response["error"])
            self.report({"ERROR"}, "request for Bevy registry data returned an error, is the Bevy Remote Protocol Plugin added and is the Bevy app running? :: " + brp_response["error"]["message"])
            return {'CANCELLED'}

        # write registry response to a file in .blend file
        if "skein-registry.json" in bpy.data.texts:
            embedded_registry = bpy.data.texts["skein-registry.json"]
            embedded_registry.clear()
            embedded_registry.write(json.dumps(brp_response["result"], indent=4))
        else:
            embedded_registry = bpy.data.texts.new("skein-registry.json")
            embedded_registry.write(json.dumps(brp_response["result"], indent=4))

        process_registry(context, brp_response["result"])

        return {'FINISHED'}

# TODO: allow configuration of url via addon settings or
# custom fetch operator?
def brp_fetch_registry_schema(host="http://127.0.0.1", port=15702):
    """Fetch the registry schema from a running Bevy application"""

    data = {"jsonrpc": "2.0", "method": "bevy/registry/schema", "params": {}}
    r = requests.post(host + ":" + str(port), json=data)
    brp_response = r.json()
    return brp_response

class ReloadSkeinRegistryJson(bpy.types.Operator):
    """Reload the registry information from skein-registry.json"""
    bl_idname = "wm.reload_skein_registry" # unique identifier. not specially named
    bl_label = "Reload Skein Registry" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    # execute is called to run the operator
    def execute(self, context):
        if "skein-registry.json" in bpy.data.texts:
            embedded_registry = json.loads(bpy.data.texts["skein-registry.json"].as_string())
            process_registry(context, embedded_registry)

        else:
            self.report({"ERROR"}, "A skein-registry.json text block with configuration was not found.")
            return {'CANCELLED'}

        return {'FINISHED'}

def process_registry(context, registry):
    """
    registry is a dict
    """

    debug = False
    if __package__ in context.preferences.addons:
        debug = context.preferences.addons[__package__].preferences.debug

    global_skein = context.window_manager.skein
    skein_property_groups = context.window_manager.skein_property_groups

    global_skein.registry = json.dumps(registry)

    component_list = []

    # Here's where we build up the PropertyGroup that
    # represents the hypothetical variants that account
    # for every possible component. These annotations
    # gain a field for every component type_path
    fake_component_enum_annotations = {
        "name": bpy.props.StringProperty(name="Name", default="Unknown"),
        "selected_type_path": bpy.props.StringProperty(name="Selected Type Path", default="Unknown"),
    }

    global_skein.components.clear()
    skein_property_groups.clear()
    for type_path, value in registry.items():
        # if "avian3d" not in type_path:
        #     continue
        try:
            property_group_or_property = make_property(
                skein_property_groups,
                registry,
                type_path
            )
            if "reflectTypes" in value and "Component" in value["reflectTypes"]:
                component = global_skein.components.add()
                component.name = type_path
                component.value = type_path
                component.type_path = type_path
                component.short_path = value["shortPath"]

                component_list.append((type_path, value["shortPath"], type_path))

                # hash type_paths that are longer than 63 characters because they
                # will make the type class registration fail:
                # TypeError: 'bevy_render::camera::manual_texture_view::ManualTextureViewHandle' too long, max length is 63
                # 
                # We try to only do it for type_paths that exceed
                # the limit, because the hash shows up in error messages, reducing readability
                # and debuggability... or blender's python implementation could allows key lengths...
                maybe_hashed_type_path = hash_over_64(type_path)
                if inspect.get_annotations(property_group_or_property):
                    fake_component_enum_annotations[maybe_hashed_type_path] = bpy.props.PointerProperty(
                        type=property_group_or_property,
                        override={"LIBRARY_OVERRIDABLE"},
                    )
                else:
                    fake_component_enum_annotations[maybe_hashed_type_path] = property_group_or_property


        except Exception as e:
            if debug:
                print("failed to make_property for: ", type_path)
                print(repr(e))
    
    # Create the type we'll use as every component
    component_container = type("ComponentContainer", (bpy.types.PropertyGroup,), {
        '__annotations__': fake_component_enum_annotations,
    })

    bpy.utils.register_class(component_container)

    # new component list data. Must be set to read component data from .blend file
    bpy.types.Object.skein_two = bpy.props.CollectionProperty(
        type=component_container,
        override={"LIBRARY_OVERRIDABLE"},
    )
    bpy.types.Mesh.skein_two = bpy.props.CollectionProperty(
        type=component_container,
        override={"LIBRARY_OVERRIDABLE"},
    )
    bpy.types.Material.skein_two = bpy.props.CollectionProperty(
        type=component_container,
        override={"LIBRARY_OVERRIDABLE"},
    )
