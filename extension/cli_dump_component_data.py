import inspect
import json
import os
import sys

import bpy

from .form_to_object import get_data_from_active_editor
from .property_groups import hash_over_64


def argparse_create():
    import argparse

    parser = argparse.ArgumentParser(
        prog=os.path.basename(sys.argv[0]) + " --command dump_component_data",
        description="Write internal component representation to a file for further inspection or processing",
    )

    parser.add_argument(
        "-o", "--output",
        dest="output",
        metavar='OUTPUT',
        type=str,
        help="The path to write the data to.",
        required=True,
    )

    parser.add_argument(
        "-p", "--type-paths",
        dest="type_paths",
        metavar='TYPE_PATHS',
        nargs='*',
        default=[],
        help="limit components by type_path",
        required=False,
    )

    return parser


def dump_component_data(argv):
    parser = argparse_create()
    args = parser.parse_args(argv)

    component_data = {}

    data = []
    for object in bpy.data.objects:
        gather(object, data, args.type_paths)
    component_data["object"] = data

    data = []
    for object in bpy.data.meshes:
        gather(object, data, args.type_paths)
    component_data["mesh"] = data

    data = []
    for object in bpy.data.materials:
        gather(object, data, args.type_paths)
    component_data["material"] = data

    data = []
    for object in bpy.data.scenes:
        gather(object, data, args.type_paths)
    component_data["scene"] = data

    data = []
    for object in bpy.data.cameras:
        gather(object, data, args.type_paths)
    component_data["camera"] = data

    data = []
    for object in bpy.data.lights:
        gather(object, data, args.type_paths)
    component_data["light"] = data

    data = []
    for object in bpy.data.collections:
        gather(object, data, args.type_paths)
    component_data["collection"] = data

    data = []
    for armature in bpy.data.armatures:
        for object in armature.bones:
            print(object)
            gather(data, object, args.type_paths)
    component_data["bone"] = data

    with open(args.output, 'w') as json_file:
        json.dump(component_data, json_file, indent=4)

    return 0

# this function is basically a copy of gltf_export_extension::gather_skein_two
# with a few changes.
# - type_path_filters allows for filtering out certain components
# - instead of adding to the "extras" of the sink, we append to a list
def gather(source, sink, type_path_filters):
    if "skein_two" in dir(source):
        objs = []
        unrecognized_components = []
        skein_property_groups = bpy.context.window_manager.skein_property_groups
        if type_path_filters and component.selected_type_path not in type_path_filters:
            return
        for component in source.skein_two:
            obj = {}
            type_path = component["selected_type_path"]

            if type_path not in skein_property_groups:
                unrecognized_components.append(type_path)
                continue
            
            if inspect.isclass(skein_property_groups[type_path]):
                try:
                    match skein_property_groups[type_path].force_default:
                        case "object":
                            obj[type_path] = {}
                        case "list":
                            obj[type_path] = []
                    objs.append(obj)
                except AttributeError:
                    value = get_data_from_active_editor(
                        component,
                        hash_over_64(type_path),
                    )
                    obj[type_path] = value
                    objs.append(obj)
            else:
                # if the component is a tuple struct, etc
                # retrieve the value directly instead of
                # recursing
                obj[type_path] = getattr(component, hash_over_64(type_path))
                objs.append(obj)

        if objs or unrecognized_components:
            output = {
                "name": source.name,
                "components": objs,
            }
            if unrecognized_components:
                output["unrecognized_components"] = unrecognized_components
            sink.append(output)

