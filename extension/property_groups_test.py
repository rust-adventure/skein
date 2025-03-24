import pytest
import bpy

from .property_groups import capitalize_path, hash_type_path, make_property
import json
import inspect

class TestClass:
    def test_capitalize(self):
        assert capitalize_path("test_components::Player") == "TestComponentsPlayer"
        assert capitalize_path("test_components::TeamMember") == "TestComponentsTeamMember"

    def test_hash(self):
        assert hash_type_path(capitalize_path("component_tests::Player")) == "SKEIN_98E71DE56C8EFC57C6540F48FDA45A5E"
        assert hash_type_path(capitalize_path("component_tests::TeamMember")) == "SKEIN_192CD808A57D7EAF156A6E4D24B8890C"

    def test_player_struct(self):
            check_fields(
                 "test_components::Player",
                 ["name", "power", "test"]
            )

    def test_team_member_struct(self):
            check_fields(
                 "test_components::TeamMember",
                 ["player", "team"]
            )
# "test_components::Player"
# "test_components::SomeThings"
# "test_components::TaskPriority"
# "test_components::Team"
# "test_components::TeamMember"
# "test_components::TupleStruct"

    def test_marker(self):
        with open("./examples/component_tests.json") as registry_json:
            registry = json.loads(registry_json.read())
            skein_property_groups = {}
            bpy.types.Scene.test_data = make_property(
                skein_property_groups,
                registry,
                'test_components::Marker'
            )
            assert "test_components::Marker" in skein_property_groups

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