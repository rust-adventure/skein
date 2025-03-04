import pytest
import bpy
from extension import capitalize_path, make_property
import math
import json
import inspect

# content of test_class.py
class TestClass:
    def test_capitalize(self):
        assert capitalize_path("component_tests::Player") == "ComponentTestsPlayer"
        assert capitalize_path("component_tests::TeamMember") == "ComponentTestsTeamMember"

    def test_player_struct(self):
        with open("./examples/component_tests.json") as registry_json:
            registry = json.loads(registry_json.read())
            skein_property_groups = {}
            bpy.types.Scene.test_data = make_property(
                skein_property_groups,
                registry,
                'component_tests::Player'
            )
            # print("skein_property_groups", skein_property_groups)
            assert "component_tests::Player" in skein_property_groups
            scene = bpy.context.scene

            test_data = inspect.get_annotations(scene.test_data)
            # print(scene.test_data.path_from_id())
            assert "name" in test_data
            assert "power" in test_data
            assert "test" in test_data

    def test_marker(self):
        with open("./examples/component_tests.json") as registry_json:
            registry = json.loads(registry_json.read())
            skein_property_groups = {}
            bpy.types.Scene.test_data = make_property(
                skein_property_groups,
                registry,
                'component_tests::Marker'
            )
            assert "component_tests::Marker" in skein_property_groups
            scene = bpy.context.scene

            test_data = inspect.get_annotations(scene.test_data)
            # test_data should be empty, and therefore falsey
            assert not test_data



# "component_tests::TupleStruct"
# "component_tests::Marker"
# "component_tests::TaskPriority"
# "component_tests::SomeThings"

# scene.test_float = 12.34
# print('test_float:', scene.test_float)
# assert math.isclose(scene.test_float, 12.34, rel_tol=1e-5)