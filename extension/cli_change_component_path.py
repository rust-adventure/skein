import inspect
import json
import os
import sys

import bpy

from .object_to_form import object_to_form
from .form_to_object import get_data_from_active_editor
from .property_groups import hash_over_64


def argparse_create():
    import argparse

    parser = argparse.ArgumentParser(
        prog=os.path.basename(sys.argv[0]) + " --command change_component_path",
        description="Change the module path of a component, keeping its data",
    )

    parser.add_argument(
        "-o", "--old_path",
        dest="old_path",
        metavar='OLD_PATH',
        type=str,
        help="The full type path of the component to change. The blend file will *no longer* include this path after this command.",
        required=True,
    )

    parser.add_argument(
        "-n", "--new_path",
        dest="new_path",
        metavar='NEW_PATH',
        type=str,
        help="The full type path of the *new* component path. The blend file will include this path after this command",
        required=True,
    )

    return parser


def change_component_path(argv):
    parser = argparse_create()
    args = parser.parse_args(argv)

    modifications = {}

    data = []
    for object in bpy.data.objects:
        change_selected_type_path(object, args.old_path, args.new_path, data)
        modifications["object"] = data
    
    data = []
    for object in bpy.data.meshes:
        change_selected_type_path(object, args.old_path, args.new_path, data)
        modifications["mesh"] = data
    
    data = []
    for object in bpy.data.materials:
        change_selected_type_path(object, args.old_path, args.new_path, data)
        modifications["material"] = data
    
    data = []
    for object in bpy.data.scenes:
        change_selected_type_path(object, args.old_path, args.new_path, data)
        modifications["scene"] = data
    
    data = []
    for object in bpy.data.cameras:
        change_selected_type_path(object, args.old_path, args.new_path, data)
        modifications["camera"] = data
    
    data = []
    for object in bpy.data.lights:
        change_selected_type_path(object, args.old_path, args.new_path, data)
        modifications["light"] = data
    
    data = []
    for object in bpy.data.collections:
        change_selected_type_path(object, args.old_path, args.new_path, data)
        modifications["collection"] = data
    
    data = []
    for armature in bpy.data.armatures:
        for object in armature.bones:
            change_selected_type_path(object, args.old_path, args.new_path, data)
            modifications["bone"] = data
    # with open(args.output, 'w') as json_file:
    #     json.dump(component_data, json_file, indent=4)

    print(modifications)
    return 0

def change_selected_type_path(object, old_path, new_path, changed):
    for component in object.skein_two:
        if component.selected_type_path == old_path:
            data = get_data_from_active_editor(
                component,
                hash_over_64(component.selected_type_path),
            )
            component.selected_type_path = new_path
            # We should set the name here even though it is arbitrary, because
            # this name is what a user sees to identify components in the UI
            # by short name
            component.name = new_path.split("::")[-1]
            object_to_form(component, hash_over_64(component.selected_type_path), data)

            # after making modifications, we must save to persist the changes
            bpy.ops.wm.save_mainfile()

            changed.append(object.name)

def touch_all_fields(context, key):
    try:
        obj = getattr(context, key)
        annotations = getattr(obj, "__annotations__")
        for key, value in annotations.items():
            if "PointerProperty" == value.function.__name__:
                touch_all_fields(obj, key)
    except:
        pass