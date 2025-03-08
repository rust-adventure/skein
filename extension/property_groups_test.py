import pytest
import bpy

from .form_to_object import get_data_from_active_editor
from .property_groups import capitalize_path, make_property
import json
import inspect

class TestClass:
    def test_capitalize(self):
        assert capitalize_path("component_tests::Player") == "ComponentTestsPlayer"
        assert capitalize_path("component_tests::TeamMember") == "ComponentTestsTeamMember"

    def test_player_struct(self):
            check_fields(
                 "component_tests::Player",
                 ["name", "power", "test"]
            )

    def test_team_member_struct(self):
            check_fields(
                 "component_tests::TeamMember",
                 ["player", "team"]
            )
# "component_tests::Player"
# "component_tests::SomeThings"
# "component_tests::TaskPriority"
# "component_tests::Team"
# "component_tests::TeamMember"
# "component_tests::TupleStruct"

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

            test_data = inspect.get_annotations(bpy.context.scene.test_data)
            # test_data should be empty, and therefore falsey
            assert not test_data

# make a PropertyGroup and check to make sure the fields are constructed
def check_fields(type_path, fields):

    with open("./examples/component_tests.json") as registry_json:
        registry = json.loads(registry_json.read())
        skein_property_groups = {}
        bpy.types.Scene.active_editor = make_property(
            skein_property_groups,
            registry,
            type_path
        )

        assert type_path in skein_property_groups

        active_editor = inspect.get_annotations(bpy.context.scene.active_editor)

        for field in fields:
            assert field in active_editor