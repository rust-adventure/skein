import bpy # type: ignore

from .form_to_object import get_data_from_active_editor
from .property_groups import make_property
import json

class TestClass:
    def test_player_struct(self):
        type_path = "test_components::Player"
        skein_property_groups = {}
        build_editor(type_path, skein_property_groups)
        bpy.context.scene.active_editor.name = "test"
        bpy.context.scene.active_editor.power = 1.0
        bpy.context.scene.active_editor.test = 20
        
        data = get_data_from_active_editor(
                bpy.context.scene,
                "active_editor",
                skein_property_groups[type_path],
                True
        )
        assert data == {
                "name": "test",
                "power": 1.0,
                "test": 20
        }

    def test_linear_velocity(self):
        type_path = "test_components::LinearVelocity"
        skein_property_groups = {}
        build_editor(type_path, skein_property_groups)
        bpy.context.scene.active_editor.x = 1.0
        bpy.context.scene.active_editor.y = 2.0
        bpy.context.scene.active_editor.z = 3.
        
        data = get_data_from_active_editor(
                bpy.context.scene,
                "active_editor",
                skein_property_groups[type_path],
                True
        )
        assert data == [1.0, 2.0, 3.0]

    # def test_team_member_component(self):
    #     type_path = "test_components::TeamMember"
    #     skein_property_groups = {}
    #     build_editor(type_path, skein_property_groups)
    #     bpy.context.scene.active_editor.player.name = "test"
    #     bpy.context.scene.active_editor.player.power = 1.0
    #     bpy.context.scene.active_editor.player.test = 20
        
    #     data = get_data_from_active_editor(
    #             bpy.context.scene,
    #             "active_editor",
    #             skein_property_groups[type_path],
    #             True
    #     )
    #     assert data == {
    #             "name": "test",
    #             "power": 1.0,
    #             "test": 20
    #     }

    # def test_some_things_enum(self):
    #         type_path = "test_components::SomeThings"
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
    #         type_path = "test_components::TaskPriority"
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
# "test_components::Player"
# "test_components::SomeThings"
# "test_components::TaskPriority"
# "test_components::Team"
# "test_components::TeamMember"
# "test_components::TupleStruct"

# make a PropertyGroup and check to make sure the fields are constructed
def build_editor(type_path, skein_property_groups):

    with open("./examples/component_tests.json") as registry_json:
        registry = json.loads(registry_json.read())
        bpy.types.Scene.active_editor = make_property(
            skein_property_groups,
            registry,
            type_path,
            None
        )

        assert type_path in skein_property_groups
