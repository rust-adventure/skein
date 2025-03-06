import pytest
import bpy
from .property_groups import capitalize_path, make_property
import json
import inspect

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

            assert "component_tests::Player" in skein_property_groups
            scene = bpy.context.scene

            test_data = inspect.get_annotations(scene.test_data)

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
