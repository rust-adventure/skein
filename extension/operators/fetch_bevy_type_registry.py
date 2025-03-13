import inspect
from pathlib import Path
import bpy
import json
import os
import requests
from ..property_groups import make_property
# --------------------------------- #
#  Fetch and store the bevy type    #
#  registry, for panel display      #
# --------------------------------- #

class FetchBevyTypeRegistry(bpy.types.Operator):
    """Fetch the Bevy type registry via the Bevy Remote Protocol"""
    bl_idname = "bevy.fetch_type_registry" # unique identifier. not specially named
    bl_label = "Fetch Bevy Type Registry" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    # execute is called to run the operator
    def execute(self, context):
        preferences = context.preferences
        addon_prefs = preferences.addons["bl_ext.user_default.bevy_skein"].preferences
        if addon_prefs.debug:
            print("\nexecute: FetchBevyTypeRegistry")

        brp_response = None

        try:
            brp_response = brp_fetch_registry_schema()
        except:
            self.report({"ERROR"}, "Could not connect to bevy application to fetch registry data from the Bevy Remote Protocol")
            return {'CANCELLED'}

        # If the bevy remote protocol returns an error, report it to the user
        if brp_response is not None and "error" in brp_response:
            if addon_prefs.debug:
                print("bevy request errored out", brp_response["error"])
            self.report({"ERROR"}, "request for Bevy registry data returned an error, is the Bevy Remote Protocol Plugin added and is the Bevy app running? :: " + brp_response["error"]["message"])
            return {'CANCELLED'}

        # write registry response to a file in .blend file
        if "skein-registry.json" in bpy.data.texts:
            embedded_registry = bpy.data.texts["skein-registry.json"]
            embedded_registry.write(json.dumps(brp_response["result"]))
        else:
            embedded_registry = bpy.data.texts.new("skein-registry.json")
            embedded_registry.write(json.dumps(brp_response["result"]))

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

def process_registry(context, registry):
    """
    registry is a dict
    """

    preferences = bpy.context.preferences
    addon_prefs = preferences.addons["bl_ext.user_default.bevy_skein"].preferences

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
    for type_path, value in registry.items():
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

                # TODO: skip type_paths that are longer than 63 characters because they
                # will make the type class registration fail:
                # TypeError: 'bevy_render::camera::manual_texture_view::ManualTextureViewHandle' too long, max length is 63
                # maybe we hash the type_paths in the future to contrain the length
                if len(type_path) <= 63:
                    if inspect.get_annotations(property_group_or_property):
                        fake_component_enum_annotations[type_path] = bpy.props.PointerProperty(type=property_group_or_property)
                    else:
                        fake_component_enum_annotations[type_path] = property_group_or_property
                else:
                    if addon_prefs.debug:
                        print("opting out for: ", type_path)
        except Exception as e:
            if addon_prefs.debug:
                print("failed to make_property for: ", type_path)
                print(repr(e))
    
    # Create the type we'll use as every component
    component_container = type("ComponentContainer", (bpy.types.PropertyGroup,), {
        '__annotations__': fake_component_enum_annotations,
    })

    bpy.utils.register_class(component_container)

    # new component list data. Must be set to read component data from .blend file
    bpy.types.Object.skein_two = bpy.props.CollectionProperty(type=component_container)
    bpy.types.Mesh.skein_two = bpy.props.CollectionProperty(type=component_container)
    bpy.types.Material.skein_two = bpy.props.CollectionProperty(type=component_container)
