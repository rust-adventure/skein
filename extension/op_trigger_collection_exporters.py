import bpy

class TriggerCollectionExporters(bpy.types.Operator):
    """Trigger all configured collection exporters for all scenes"""
    bl_idname = "wm.skein_trigger_collection_exporters" # unique identifier. first word is required by extensions review team to be from a specific set of words
    bl_label = "Trigger All Collection Exporters" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    def execute(self, context):
        debug = False
        if __package__ in bpy.context.preferences.addons:
            preferences = bpy.context.preferences.addons[__package__].preferences
            debug = preferences.debug

        if debug:
            print("skein: triggering all collection exporters for all scenes")
        # The collection_export_all depends on the current layer_collection,
        # which we drive by setting the scene.
        for scene in bpy.data.scenes:
            with context.temp_override(scene=scene):
                bpy.ops.wm.collection_export_all()
        return {'FINISHED'}

classes = (
    TriggerCollectionExporters,
)

register, unregister = bpy.utils.register_classes_factory(classes)