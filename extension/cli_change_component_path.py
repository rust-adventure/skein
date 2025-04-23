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
        "-f", "--from",
        dest="from",
        metavar='FROM',
        nargs='*',
        default=[],
        help="The full type path of the component to change. The blend file will *no longer* include this path after this command.",
        required=True,
    )

    parser.add_argument(
        "-i", "--into",
        dest="into",
        metavar='INTO',
        nargs='*',
        default=[],
        help="The full type path of the *new* component path. The blend file will include this path after this command",
        required=True,
    )

    return parser


def dump_component_data(argv):
    parser = argparse_create()
    args = parser.parse_args(argv)

    component_data = {}

    data = []
    for object in bpy.data.objects:
        gather(data, object, args.type_paths)
    component_data["object"] = data

    data = []
    for object in bpy.data.meshes:
        gather(data, object, args.type_paths)
    component_data["mesh"] = data

    data = []
    for object in bpy.data.materials:
        gather(data, object, args.type_paths)
    component_data["material"] = data

    data = []
    for object in bpy.data.cameras:
        gather(data, object, args.type_paths)
    component_data["camera"] = data

    data = []
    for object in bpy.data.lights:
        gather(data, object, args.type_paths)
    component_data["light"] = data

    data = []
    for object in bpy.data.collections:
        gather(data, object, args.type_paths)
    component_data["collection"] = data

    with open(args.output, 'w') as json_file:
        json.dump(component_data, json_file, indent=4)

    return 0

def gather(object_data, object, type_path_filters):
    pass
    # components = []
    # for component in object.skein_two:
    #     skein_property_groups = bpy.context.window_manager.skein_property_groups
    #     if type_path_filters and component.selected_type_path not in type_path_filters:
    #         return
    #     if inspect.isclass(skein_property_groups[component.selected_type_path]):
    #         components.append({
    #             "type_path": component.selected_type_path,
    #             "data": get_data_from_active_editor(
    #                 component,
    #                 hash_over_64(component.selected_type_path),
    #             )
    #         })
    #     else:
    #         components.append({
    #             "type_path": component.selected_type_path,
    #             "data": getattr(component, component.selected_type_path)
    #         })
    # if components:
    #     object_data.append({
    #         "name": object.name,
    #         "components": components
    #     })