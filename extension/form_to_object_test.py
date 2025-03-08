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
            type_path = "component_tests::Player"
            skein_property_groups = {}
            build_editor(type_path, skein_property_groups)
            print(skein_property_groups)
            bpy.context.scene.active_editor.name = "test"
            bpy.context.scene.active_editor.power = 1.0
            bpy.context.scene.active_editor.test = 20
            
            data = get_data_from_active_editor(
                 bpy.context.scene,
                 "active_editor",
                 skein_property_groups[type_path]
            )
            assert data == {
                 "name": "test",
                 "power": 1.0,
                 "test": 20
            }

    # def test_some_things_enum(self):
    #         type_path = "component_tests::SomeThings"
    #         skein_property_groups = {}
    #         build_editor(type_path, skein_property_groups)
    #         print(skein_property_groups)
    #         bpy.context.scene.active_editor.skein_enum_index = "OneThing"
    #         bpy.context.scene.active_editor.name = "test"
            
    #         data = get_data_from_active_editor(
    #              bpy.context.scene,
    #              "active_editor",
    #              skein_property_groups[type_path]
    #         )
    #         assert data == {
    #              "name": "test",
    #              "power": 1.0,
    #              "test": 201
    #         }

    # def test_task_priority(self):
    #         type_path = "component_tests::TaskPriority"
    #         skein_property_groups = {}
    #         build_editor(type_path, skein_property_groups)
    #         print(skein_property_groups)
    #         bpy.context.scene.active_editor = "High"
            
    #         data = get_data_from_active_editor(
    #              bpy.context.scene,
    #              "active_editor",
    #              skein_property_groups[type_path]
    #         )
    #         assert data == {
    #              "name": "test",
    #              "power": 1.0,
    #              "test": 201
    #         }
# "component_tests::Player"
# "component_tests::SomeThings"
# "component_tests::TaskPriority"
# "component_tests::Team"
# "component_tests::TeamMember"
# "component_tests::TupleStruct"

# make a PropertyGroup and check to make sure the fields are constructed
def build_editor(type_path, skein_property_groups):

    with open("./examples/component_tests.json") as registry_json:
        registry = json.loads(registry_json.read())
        bpy.types.Scene.active_editor = make_property(
            skein_property_groups,
            registry,
            type_path
        )

        assert type_path in skein_property_groups
