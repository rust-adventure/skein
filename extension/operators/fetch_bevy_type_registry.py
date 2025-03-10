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
        print("\nexecute: FetchBevyTypeRegistry")

        brp_response = None

        try:
            brp_response = brp_fetch_registry_schema()
        except:
            self.report({"ERROR"}, "Could not connect to bevy application to fetch registry data from the Bevy Remote Protocol")
            return {'CANCELLED'}

        # If the bevy remote protocol returns an error, report it to the user
        if brp_response is not None and "error" in brp_response:
            print("bevy request errored out", brp_response["error"])
            self.report({"ERROR"}, "request for Bevy registry data returned an error, is the Bevy Remote Protocol Plugin added and is the Bevy app running? :: " + brp_response["error"]["message"])
            return {'CANCELLED'}

        registry_filepath = bpy.path.abspath(os.path.join("//", "skein-registry.json"))

        with open(registry_filepath,"w") as outfile:
            json.dump(brp_response["result"], outfile)

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

    global_skein = context.window_manager.skein
    skein_property_groups = context.window_manager.skein_property_groups

    global_skein.registry = json.dumps(registry)

    component_list = []

    global_skein.components.clear()
    for k, value in registry.items():
        # TODO: this must apply to all components
        # make_property is recursive, so all dependent types
        # should make it into the skein_property_groups
        # if k in [
        #     "component_tests::Player",
        #     "component_tests::TaskPriority",
        #     "component_tests::TeamMember",
        #     "component_tests::TupleStruct",
        #     "component_tests::Marker",
        #     "component_tests::SomeThings",
        #     "test_project::Rotate"
        # ]:
        try:
            make_property(
                skein_property_groups,
                registry,
                k
            )
            if "reflectTypes" in value and "Component" in value["reflectTypes"]:
                component = global_skein.components.add()
                component.name = k
                component.value = k
                component.type_path = k
                component.short_path = value["shortPath"]

                component_list.append((k, value["shortPath"], k))
        except Exception as e:
            print("failed to make_property for: ", k)
            print(repr(e))
