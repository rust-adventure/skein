import inspect
from pathlib import Path
import bpy # type: ignore
import json
import requests # type: ignore
import os
from .property_groups import hash_over_64, make_property
# --------------------------------- #
#  Fetch and store the bevy type    #
#  registry, for panel display      #
# --------------------------------- #

class FetchRemoteTypeRegistry(bpy.types.Operator):
    """Fetch a Bevy type registry from a compatible endpoint"""
    bl_idname = "wm.fetch_type_registry" # unique identifier. not specially named
    bl_label = "Fetch a Remote Type Registry" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    # execute is called to run the operator
    def execute(self, context):
        debug = False
        if __package__ in context.preferences.addons:
            debug = context.preferences.addons[__package__].preferences.debug

        if debug:
            print("\nexecute: FetchRemoteTypeRegistry")

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
    """Reload the registry information from skein-registry.json and re-process it"""
    bl_idname = "wm.reload_skein_registry" # unique identifier. not specially named
    bl_label = "Reload Local Skein Registry" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    # execute is called to run the operator
    def execute(self, context):
        # if a skein-registry.json was already created, use it as the source of truth
        if "skein-registry.json" in bpy.data.texts:
            embedded_registry = json.loads(bpy.data.texts["skein-registry.json"].as_string())
            process_registry(context, embedded_registry)
        else:
            # if we're trying to reload the registry file, and we haven't created one yet
            # insert some demo data, which in turn means that the file will be created and
            # is easier to access and modify by users who wish to do so.
            dirname = os.path.dirname(__file__)
            filename = os.path.join(dirname, 'default_registry.json')
            with open(filename) as default_registry_file:
                data = json.loads(default_registry_file.read())
                embedded_registry = bpy.data.texts.new("skein-registry.json")
                embedded_registry.write(json.dumps(data, indent=4))
                # read the file we just wrote, so that this code doesn't need to be updated in
                # the future. If its in the skein-registry.json, then it will be processed
                embedded_registry = json.loads(bpy.data.texts["skein-registry.json"].as_string())
                process_registry(context, embedded_registry)

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
    #
    # this approach is required because Blender's implementation
    # of Python and Properties *does not* include modern language
    # features like ADTs (aka: enums that can carry data).
    fake_component_enum_annotations = {
        "name": bpy.props.StringProperty(name="Name", default="Unknown"),
        "selected_type_path": bpy.props.StringProperty(name="Selected Type Path", default="Unknown"),
    }

    # clear the list we use as a component type selector for the UI
    # because we are about to re-fill it.
    global_skein.components.clear()
    # unregister all of the PropertyGroups that were created the
    # last time we processed a registry schema
    for type_path, property_group in skein_property_groups.items():
        try:
            bpy.utils.unregister_class(property_group)
        except:
            # unregister_class is recursive and we re-use classes
            # in many cases. So unregistering one class that uses 
            # another causes that class to *already* be unregistered
            # when we go to unregister it directly.
            pass

    # Clear the list that held the PropertyGroups because we are about
    # to re-fill it.
    skein_property_groups.clear()

    # for each user-defined type, make a PropertyGroup that represents
    # that type. These will be used to build out user-accessible forms
    # allowing users to edit their structured data
    for type_path, value in registry.items():
        # TODO: for debugging purposes, it can be useful to filter
        # the schema being processed without modifying the schema 
        # file. Only types that pass this test will be processed.
        # This should become an addon preference to allow users
        # to gain information should they want to
        #
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

    # adding the container to the `skein_property_groups` list
    # means it will get unregistered alongside other data.
    # We don't rely on this list being "only component types"
    # so adding to it is fine
    skein_property_groups["skein_internal_container"] = component_container
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
    bpy.types.Camera.skein_two = bpy.props.CollectionProperty(
        type=component_container,
        override={"LIBRARY_OVERRIDABLE"},
    )
    bpy.types.Light.skein_two = bpy.props.CollectionProperty(
        type=component_container,
        override={"LIBRARY_OVERRIDABLE"},
    )
    bpy.types.Collection.skein_two = bpy.props.CollectionProperty(
        type=component_container,
        override={"LIBRARY_OVERRIDABLE"},
    )
