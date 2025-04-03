import inspect
import json
import unittest
import bpy
import sys
import os

# this adds the extension to the path so we can import it
# to call the require function
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from extension import register as breg, unregister as bunreg
from extension.fetch_bevy_type_registry import process_registry
from extension.form_to_object import get_data_from_active_editor

snapshots = {}
with open("tools/combined_snapshots.json") as snapshots_file:
    snapshots = json.loads(snapshots_file.read())

class ComponentPropertyTests(unittest.TestCase):
    def test_linear_velocity(self):

        bpy.context.window_manager.selected_component = "test_components::LinearVelocity";
        bpy.ops.bevy.insert_bevy_component()

        container = bpy.context.active_object.skein_two[0]

        # load-bearing getattr
        # without this getattr, the object doesn't actually get initialized
        obj = getattr(container, "test_components::LinearVelocity")
        obj.x = 2.

        data = get_data_from_active_editor(
            container,
            container.selected_type_path
        )

        self.assertEqual(data, [2.0, 0.0, 0.0])
        bpy.ops.bevy.remove_bevy_component()

    def test_snapshots(self):
        self.maxDiff = None
        for snapshot in snapshots:

            with self.subTest(snapshot):  
                # assert test.expected == make_relative(path=test.path, root=test.root)
                # each snapshot is a single key/value pair
                for key, value in snapshot.items():

                    bpy.context.window_manager.selected_component = key;
                    bpy.ops.bevy.insert_bevy_component()

                    container = bpy.context.active_object.skein_two[0]

                    try:
                        if inspect.isclass(bpy.context.window_manager.skein_property_groups[container.selected_type_path]):
                            # load-bearing getattrs
                            # without this, the PointerProperty values
                            # don't actually get initialized
                            touch_all_fields(container, key)

                            data = get_data_from_active_editor(
                                container,
                                container.selected_type_path
                            )
                            self.assertEqual(data, value)
                        else:
                            data = getattr(container, container.selected_type_path)
                            self.assertEqual(data, value)
                    except Exception as e:
                        raise
                    finally:
                        # always remove the bevy component,
                        # we're working in a headless blender
                        # context so we have to clean up shared 
                        # resources ourselves
                        bpy.ops.bevy.remove_bevy_component()

# getattr on anything that is a PointerProperty
#
# blender requires us to touch all fields 
# to be able to read the values, otherwise they
# won't be initialized. This usually happens 
# when displaying them in the UI with
# layout.prop/render_props but we need to hack it
# manually here for tests
def touch_all_fields(context, key):
    try:
        obj = getattr(context, key)
        annotations = getattr(obj, "__annotations__")
        for key, value in annotations.items():
            if "PointerProperty" == value.function.__name__:
                touch_all_fields(obj, key)
    except:
        pass

if __name__ == '__main__':
    import sys
    sys.argv = [__file__] + (sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])

    breg()

    content = ""
    with open("registry.json") as my_file:
        content = json.loads(my_file.read())

    process_registry(bpy.context, content)

    unittest.main()

