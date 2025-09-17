import bpy # type: ignore
import json

# ---------------------------------- #
#  Skein Panel for adding components #
#  This shows in the Properties      #
#  tabs for the relevant objects     #
# ---------------------------------- #

class SkeinPanelPresetsObject(bpy.types.Panel):
    """Creates a Panel in the Object Properties Panel for an object"""
    bl_label = "Skein Component Preset Panel"
    bl_idname = "OBJECT_PT_skein_preset_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_context = 'object'

    @classmethod
    def poll(cls, context):
        return bpy.ops.object.insert_component.poll() and "skein-presets.json" in bpy.data.texts

    def draw(self, context):
        obj = context.object
        draw_generic_panel(context, obj, self.layout, "object")

class SkeinPanelPresetsMesh(bpy.types.Panel):
    """Creates a Panel in the Object Properties Panel for a mesh"""
    bl_label = "Skein Component Preset Panel"
    bl_idname = "MESH_PT_skein_preset_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_context = 'data'

    @classmethod
    def poll(cls, context):
        return bpy.ops.mesh.insert_component.poll() and "skein-presets.json" in bpy.data.texts

    def draw(self, context):
        obj = context.mesh
        draw_generic_panel(context, obj, self.layout, "mesh")

class SkeinPanelPresetsMaterial(bpy.types.Panel):
    """Creates a Panel in the Object Properties Panel for a material"""
    bl_label = "Skein Component Preset Panel"
    bl_idname = "MATERIAL_PT_skein_preset_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_context = 'material'

    @classmethod
    def poll(cls, context):
        return bpy.ops.material.insert_component.poll() and "skein-presets.json" in bpy.data.texts

    def draw(self, context):
        obj = context.material
        draw_generic_panel(context, obj, self.layout, "material")

class SkeinPanelPresetsScene(bpy.types.Panel):
    """Creates a Panel in the Object Properties Panel for a scene"""
    bl_label = "Skein Component Preset Panel"
    bl_idname = "SCENE_PT_skein_preset_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_context = 'scene'

    @classmethod
    def poll(cls, context):
        return bpy.ops.scene.insert_component.poll() and "skein-presets.json" in bpy.data.texts

    def draw(self, context):
        obj = context.scene
        draw_generic_panel(context, obj, self.layout, "scene")

class SkeinPanelPresetsLight(bpy.types.Panel):
    """Creates a Panel in the Object Properties Panel for a light"""
    bl_label = "Skein Component Preset Panel"
    bl_idname = "LIGHT_PT_skein_preset_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_context = 'data'

    @classmethod
    def poll(cls, context):
        return bpy.ops.light.insert_component.poll() and "skein-presets.json" in bpy.data.texts

    def draw(self, context):
        obj = context.light
        draw_generic_panel(context, obj, self.layout, "light")

class SkeinPanelPresetsCollection(bpy.types.Panel):
    """Creates a Panel in the Object Properties Panel for a collection"""
    bl_label = "Skein Component Preset Panel"
    bl_idname = "COLLECTION_PT_skein_preset_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_context = 'collection'

    @classmethod
    def poll(cls, context):
        return bpy.ops.collection.insert_component.poll() and "skein-presets.json" in bpy.data.texts

    def draw(self, context):
        obj = context.collection
        draw_generic_panel(context, obj, self.layout, "collection")

class SkeinPanelPresetsBone(bpy.types.Panel):
    """Creates a Panel in the Object Properties Panel for a bone"""
    bl_label = "Skein Component Preset Panel"
    bl_idname = "BONE_PT_skein_preset_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_context = 'bone'

    @classmethod
    def poll(cls, context):
        return bpy.ops.bone.insert_component.poll() and "skein-presets.json" in bpy.data.texts

    def draw(self, context):
        # we use context.bone because context.active_bone will return 
        # an EditBone *or* a Bone and we want a Bone
        obj = context.bone
        draw_generic_panel(context, obj, self.layout, "bone")

def draw_generic_panel(context, obj, layout, execute_mode):
    global_skein = context.window_manager.skein
    # TODO: the registry can likely be loaded into a dict in a less
    # common place. This function runs every draw
    registry = json.loads(global_skein.registry)
    obj_skein = obj.skein_two

    presets = json.loads(bpy.data.texts["skein-presets.json"].as_string())
    if registry and obj_skein:
        active_component_data = obj_skein[obj.active_component_index]
        type_path = active_component_data.selected_type_path
        if type_path in presets:
            
            layout.emboss = 'PULLDOWN_MENU'
            layout.operator_context = 'EXEC_DEFAULT'

            for key in presets[type_path].keys():
                op = layout.operator(execute_mode + ".apply_preset", text=key)
                op.preset_id = key

            layout.operator_context = 'INVOKE_DEFAULT'
            layout.emboss = 'NORMAL'


        
