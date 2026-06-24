import bpy

class BakeAllLightmaps(bpy.types.Operator):
    """Bake all configured Lightmaps"""
    bl_idname = "wm.bake_lightmaps" # unique identifier. first word needs to be from a specific list to appear in keybinds, etc.
    bl_label = "Bake All Lightmaps" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    # not sure what the right "poll" is for a global method like this
    # @classmethod
    # def poll(cls, context):
    #     return context.object is not None

    def execute(self, context):
        # Bake for all meshes, no filter yet
        # Future: bake for meshes with "lightmap" checked
        for object in bpy.data.objects:
            if object.type != "MESH":
                print("skipping", object.type, " named ", object.name)
                # If this isn't a MESH, we can't continue
                continue
            else:
                print("baking", object.name)

            # We use the filename multiple times, so
            # store it for re-use
            filename = f"{object.name}.lightmap.png"

            # get or create the image target for the bake
            image = bpy.data.images.get(filename)
            if not image:
                print("making new image for ", filename)
                image = bpy.data.images.new(
                    filename,
                    width=1024,
                    height=1024,
                    alpha=False
                )
            # set the image target as a node in the node_tree
            # and make sure it is "active" for the bake
            node_tree = object.active_material.node_tree
            image_node = node_tree.nodes.get(image.name)
            if not image_node:
                print("making new image_node for ", filename)
                image_node = node_tree.nodes.new("ShaderNodeTexImage")
                image_node.name = image.name
            image_node.image = image
            image_node.select = True
            node_tree.nodes.active = image_node
            
            # set current object to be "selected" by overriding
            # "the context" just for the operator
            context_override = bpy.context.copy()
            context_override["selected_objects"] = [object]

            with bpy.context.temp_override(**context_override):
                # bake image
                bpy.ops.object.bake(
                    type="COMBINED",
                    pass_filter={"DIRECT", "INDIRECT", "DIFFUSE"},
                    save_mode="EXTERNAL",
                    filepath=filename,
                    width=1024,
                    height=1024,
                )
        return {'FINISHED'}

