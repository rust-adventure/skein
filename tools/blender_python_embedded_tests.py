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
from extension.property_groups import hash_over_64

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
                for type_path, value in snapshot.items():

                    bpy.context.window_manager.selected_component = type_path;
                    bpy.ops.bevy.insert_bevy_component()

                    maybe_hashed_type_path = hash_over_64(type_path)

                    container = bpy.context.active_object.skein_two[0]

                    try:
                        if inspect.isclass(bpy.context.window_manager.skein_property_groups[container.selected_type_path]):
                            data = get_data_from_active_editor(
                                container,
                                maybe_hashed_type_path
                            )
                            self.assertEqual(data, value)
                        else:
                            data = getattr(container, maybe_hashed_type_path)
                            self.assertEqual(data, value)
                    except Exception as e:
                        raise
                    finally:
                        # always remove the bevy component,
                        # we're working in a headless blender
                        # context so we have to clean up shared 
                        # resources ourselves
                        bpy.ops.bevy.remove_bevy_component()

if __name__ == '__main__':
    import sys
    sys.argv = [__file__] + (sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])

    breg()

    content = ""
    with open("registry.json") as my_file:
        content = json.loads(my_file.read())

    process_registry(bpy.context, content)

    unittest.main()

