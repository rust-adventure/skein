import bpy
import requests
import json
import re
import inspect
import string

# glTF extensions are named following a convention with known prefixes.
# See: https://github.com/KhronosGroup/glTF/tree/main/extensions#about-gltf-extensions
# also: https://github.com/KhronosGroup/glTF/blob/main/extensions/Prefixes.md
glTF_extension_name = "EXT_skein"

# is this extension required to view the glTF?
extension_is_required = False

# TODO: registry filepath should be 
# bpy.path.abspath(os.path.join("//", "skein-registry.json"))
registry_filepath = "/Users/chris/github/christopherbiscardi/skein/skein-registry.json"

# gltf exporter extension
#
# The extension takes the data from the format we need to use inside of Blender
# which can include arbitrary "active_index" selections for lists, etc and
# rewrites the skein data into a format bevy can parse and reflect directly.
#
# exported gltf extras output will look like this:
#
# ```json
# "extras":{
#   "skein":[{
#     "test_project::Rotate":{
#       "speed":1.0
#     }
#   }],
# },
# ```
class SkeinExtensionProperties(bpy.types.PropertyGroup):
    enabled: bpy.props.BoolProperty(
        name="skein",
        description='Rewrite Skein data into a directly Bevy reflectable format',
        default=True
        )

# Draw the Skein settings options in the glTF export panel
def draw_export(context, layout):

    # Note: If you are using Collection Exporter, you may want to restrict UI for some collections
    # You can access the collection like this: context.collection
    # So you can check if you want to show the UI for this collection or not, using
    # if context.collection.name != "Coll":
    #     return

    header, body = layout.panel("GLTF_addon_example_exporter", default_closed=False)

    # TODO: True or False here (and in panels)? Affects visual layout
    header.use_property_split = False

    props = bpy.context.scene.skein_extension_properties

    header.prop(props, 'enabled')
    # if body != None:
    #     body.prop(props, 'float_property', text="Some float value")


# Note: the class must have this exact name
class glTF2ExportUserExtension:
    def pre_export_hook(self, export_settings):
        print("pre_export_hook in class", export_settings)

    def __init__(self):
        print("initgltf2 export user extension")
        # We need to wait until we create the gltf2UserExtension to import the gltf2 modules
        # Otherwise, it may fail because the gltf2 may not be loaded yet
        from io_scene_gltf2.io.com.gltf2_io_extensions import Extension
        self.Extension = Extension
        self.properties = bpy.context.scene.skein_extension_properties

    def gather_node_hook(self, gltf2_object, blender_object, export_settings):
        print("gather_node_hook")
        # Note: If you are using Collection Exporters, you may want to restrict the export for some collections
        # You can access the collection like this: export_settings['gltf_collection']
        # So you can check if you want to use this hook for this collection or not, using
        # if export_settings['gltf_collection'] != "Coll":
        #     return

        # TODO: can we report needing custom_properties enabled
        # self.report() doesn't seem available here?
        if self.properties.enabled and "skein" in gltf2_object.extras:
            print("--")
            print(gltf2_object.extras)
            print("--")
            objs = []
            for node in gltf2_object.extras["skein"]:
                obj = {}
                type_path = node["type_path"]
                obj[type_path] = node["value"]
                objs.append(obj)
            gltf2_object.extras["skein"] = objs
            
            # if gltf2_object.extensions is None:
            #     gltf2_object.extensions = {}
            # gltf2_object.extensions[glTF_extension_name] = self.Extension(
            #     name=glTF_extension_name,
            #     # extension={"float": self.properties.float_property},
            #     extension={"float": 2.0},
            #     required=extension_is_required
            # )

    def glTF2_pre_export_callback(export_settings):
        print("This will be called before exporting the glTF file.2")

    def glTF2_post_export_callback(export_settings):
        print("This will be called after exporting the glTF file.")

def pre_export_hook(self, export_settings):
    print("pre_export_hook", export_settings)
def glTF2_pre_export_callback(export_settings):
    print("idk2")
# /end gltf exporter extension


def update_component_data(self, context):
    # context.obj.skein.something
    print("updating component data")
    obj = context.object
    obj_skein = obj["skein"]
    active_component_index = obj.active_component_index
    global_skein = context.window_manager.skein
    registry = json.loads(global_skein.registry)
    skein_property_groups = context.window_manager.skein_property_groups
    active_component = obj_skein[active_component_index]
    type_path = active_component["type_path"]
    active_editor = context.window_manager.active_editor

# 'BoolProperty'
# 'BoolVectorProperty'
# 'CollectionProperty'
# 'EnumProperty'
# 'FloatProperty'
# 'FloatVectorProperty'
# 'IntProperty'
# 'IntVectorProperty'
# 'PointerProperty'
# 'RemoveProperty'
# 'StringProperty'

    # print("active_editor: ")
    # print(active_editor)
    # print(active_editor.player.name)
    # for property in active_editor.bl_rna.properties:
    #     if property.is_runtime: 
    #         print("\n-")
    #         print(property)
    #         print(dir(property))
    #         print(type(property))

    if obj_skein:
        active_component_data = obj_skein[active_component_index]
        type_path = active_component_data["type_path"]
        registry_component_reflection_data = registry[type_path]
        
        if type_path in skein_property_groups:
            if inspect.isclass(skein_property_groups[type_path]):
                data = get_data_from_active_editor(context.window_manager,"active_editor",skein_property_groups[type_path])
                # print("data")
                # print(data)
                # TODO: this may only work for Structs
                # component_fields = inspect.get_annotations(skein_property_groups[type_path])
                # new_data = {}
                # for key in component_fields:
                #     new_data[key] = getattr(active_editor, key)
                #     print(new_data)
                active_component["value"] = data
            else:
                active_component["value"] = active_editor

def get_data_from_active_editor(context, context_key, component_data):

    data = {}

    if context_key != "active_editor":
        for key,value in getattr(getattr(context, context_key), "__annotations__").items():
            data[key] = getattr(getattr(context, context_key), key)

    component_fields = inspect.get_annotations(component_data)

    # TODO: move skein_enum_index logic to exporter maybe?
    # possibly useful for moving active_form to components list
    # This `if` changes the fields that are fetched, specifically
    # so that we only export one of the variants in an enum (all variants
    # have their own key in the object)
    if "skein_enum_index" in component_fields:
        active_enum_variant = getattr(getattr(context, context_key), "skein_enum_index")
        component_fields = {
            active_enum_variant: component_fields[active_enum_variant]
        }

    if component_fields:
        for key in component_fields:
            # print("key in component_fields: ", key, component_fields[key])
            if "PointerProperty" == component_fields[key].function.__name__:
                # print("  - is PointerProperty")                
                data[key] = get_data_from_active_editor(getattr(context, context_key), key, component_fields[key])
            else:
                # print("  - not PointerProperty")
                data[key] = getattr(getattr(context, context_key), key)
    else:
        # print("no component fields, not rendering: ", context, context_key)
        # TODO: figure out if this actually means there's nothing to render
        pass

    return data

class ComponentTypeData(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name", default="Unknown")
    value: bpy.props.StringProperty(name="Value", default="Unknown")
    type_path: bpy.props.StringProperty(name="Type Path", default="Unknown")
    short_path: bpy.props.StringProperty(name="Short Path", default="Unknown")

class ComponentData(bpy.types.PropertyGroup):
    type_path: bpy.props.StringProperty(name="type_path", default="Unknown")
    name: bpy.props.StringProperty(name="Name", default="Unknown")
    # value: bpy.props.StringProperty(name="Component Data")

class PGSkeinWindowProps(bpy.types.PropertyGroup):
    registry: bpy.props.StringProperty(name="Bevy Registry", default="{}")
    components: bpy.props.CollectionProperty(type=ComponentTypeData)

class TestInnerComponentData(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name", default="Unknown")
    flt: bpy.props.FloatProperty(default=0.)
    # value: bpy.props.StringProperty(name="Component Data")

class TestWrapperComponentData(bpy.types.PropertyGroup):
    type_path: bpy.props.StringProperty(name="type_path", default="Unknown")
    name: bpy.props.StringProperty(name="Name", default="Unknown")
    value: bpy.props.PointerProperty(type=TestInnerComponentData)
    # value: bpy.props.StringProperty(name="Component Data")


def update_component_form(self, context):
    print("\n## update component form")
    obj = context.object
    obj_skein = obj["skein"]
    active_component_index = obj.active_component_index
    global_skein = context.window_manager.skein
    registry = json.loads(global_skein.registry)
    skein_property_groups = context.window_manager.skein_property_groups
    active_component = obj_skein[active_component_index]
    type_path = active_component["type_path"]

    print("- type_path: " + type_path)

    # active_component.__dict__["value"] = bpy.props.StringProperty(default="hello")
    # print(skein_property_groups[type_path])
    # print(skein_property_groups[type_path].__annotations__)
    # TODO: What happens when we get data from object
    # and insert it
    # print("isclass", inspect.isclass(skein_property_groups[type_path]), skein_property_groups[type_path])

    if inspect.isclass(skein_property_groups[type_path]):
        bpy.types.WindowManager.active_editor = bpy.props.PointerProperty(
            type=skein_property_groups[type_path],
        )

        # TODO: get data from custom properties
        # TODO: set up recursive/nested forms
        # component_fields = inspect.get_annotations(skein_property_groups[type_path])
        # print("-- component_fields:")
        # for key, value in component_fields.items():

        #     # if key not in bpy.types.WindowManager.active_editor:
        #     #     print("next key not in active_editor; this usually means its a PropertyGroup class and not a primitive")
        #     print("   - " + key)
        #     print(registry[type_path])
        #     registry_component_data = registry[type_path]
        #     # We kind of already know this is a Struct because its an inspect.isclass from earlier
        #     if registry_component_data["kind"] == "Struct":
        #         # TODO: switch on registry[type_path]'s type
        #         field_type_path = registry[type_path]["properties"][key]["type"]["$ref"].removeprefix("#/$defs/")


                # if inspect.isclass(skein_property_groups[field_type_path]):
                # #     print("isclass")
                # #     print(value)
                # #     # print(getattr(bpy.types.WindowManager.active_editor, key))
                # #     # print(context.window_manager.active_editor.team)
                # #     # print(context.window_manager.active_editor)
                # #     # print(context.window_manager.active_editor.player)
                #     context.window_manager.active_editor[key] = bpy.props.PointerProperty(
                #         type=skein_property_groups[field_type_path],
                #     )
    else:
        bpy.types.WindowManager.active_editor = skein_property_groups[type_path]
    print("active_component_index", active_component_index)

def on_select_new_component(self, context):
    """Executed when a new component is selected for insertion onto an object"""
    print("\n####### on_select_new_component")
    selected_component = context.window_manager.selected_component;
    global_skein = context.window_manager.skein
    if global_skein.registry:
        print("\nregistry character:")
        data = json.loads(global_skein.registry)
        if len(data.keys()) > 0:
            # print(data["event_ordering::PowerLevel"])
            print(data[selected_component])
        else:
            print("no data in registry")
    print("######\n")
    

# --------------------------------- #
#  Fetch and store the bevy type    #
#  registry, for panel display      #
# --------------------------------- #

class FetchBevyTypeRegistry(bpy.types.Operator):
    """Fetch the Bevy type registry via the Bevy Remote Protocol"""
    bl_idname = "bevy.fetch_type_registry" # unique identifier. not specially named
    bl_label = "Fetch Bevy Type Registry" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    # execute is called to run the operator
    def execute(self, context):
        print("\nexecute: FetchBevyTypeRegistry")
        # scene = context.scene
        # cursor = scene.cursor.location
        # obj = context.active_object
        global_skein = context.window_manager.skein
        skein_property_groups = context.window_manager.skein_property_groups

        data = {"jsonrpc": "2.0", "method": "bevy/registry/schema", "params": {}}
        r = requests.post('http://127.0.0.1:15702', json=data)
        brp_response = r.json()

        # If the bevy remote protocol returns an error, report it to the user
        if "error" in brp_response:
            print("bevy request errored out", brp_response["error"])
            self.report({"ERROR"}, "request for Bevy registry data errored out, is the Bevy Remote Protocol Plugin added and is the Bevy app running? :: " + json["error"]["message"])

        with open(registry_filepath,"w") as outfile:
            json.dump(brp_response["result"], outfile)
            print(outfile)

        global_skein.registry = json.dumps(brp_response["result"])

        component_list = []

        global_skein.components.clear()
        for k, value in brp_response["result"].items():
            # TODO: this must apply to all components
            # make_property is recursive, so all dependent types
            # should make it into the skein_property_groups
            if k in [
                "component_tests::Player",
                "component_tests::TaskPriority",
                "component_tests::TeamMember",
                "component_tests::TupleStruct",
                "component_tests::Marker",
                "component_tests::SomeThings",
                "test_project::Rotate"
            ]:
                # TODO: is registering classes here enough, or
                # are there more types in the recursive make_property
                # that need to be registered?
                print("\n make_property", k)
                new_property = make_property(
                    skein_property_groups,
                    brp_response["result"],
                    k
                )
                # # if its a class we constructed, it has
                # # to be registered. If its not, it can't
                # # be registered without errors
                # print("registering")
                # print(new_property)
                # if inspect.isclass(new_property):
                #     bpy.utils.register_class(
                #         new_property
                #     )

            if "reflectTypes" in value and "Component" in value["reflectTypes"]:
                component = global_skein.components.add()
                component.name = k
                component.value = k
                component.type_path = k
                component.short_path = value["shortPath"]

                component_list.append((k, value["shortPath"], k))

        # bpy.types.WindowManager.skein_components = bpy.props.EnumProperty(
        #     items=component_list,
        #     description="A Component to add to the object",
        #     # default="()",
        #     # update=execute_operator
        # )

        print("execute/end: FetchBevyTypeRegistry\n")

        # blender uses strings to indicate when operation is done
        return {'FINISHED'}

# --------------------------------- #
#  Add hardcoded test component     #
#  to object                        #
# --------------------------------- #

class InsertBevyComponent(bpy.types.Operator):
    """Insert a hardcoded component on the object (for development)"""
    bl_idname = "bevy.insert_bevy_component" # unique identifier. not specially named
    bl_label = "Insert Bevy Component (Dev)" # Shows up in the UI
    bl_options = {'REGISTER', 'UNDO'} # enable undo (which we might not need)

    # execute is called to run the operator
    def execute(self, context):
        print("\nexecute: InsertBevyComponent")
        # scene = context.scene
        # cursor = scene.cursor.location
        obj = context.active_object
        global_skein = context.window_manager.skein
        selected_component = context.window_manager.selected_component
        obj_skein = obj.skein

        if global_skein.registry:
            registry = json.loads(global_skein.registry)
            if list(registry) and registry[selected_component]:
                data = registry[selected_component]
                print(data)
                component = obj.skein.add()
                component.name = data["shortPath"]
                component.type_path = selected_component
                # TODO: This needs to be the default data for a given component
                # component.value = json.dumps({
                #     "name": "Hollow Knight"
                # })
                # If we inserted a new component, update the 
                # active_component_index to show the right editor
                # for the newly inserted component
                obj.active_component_index = len(obj_skein) - 1

            else:
                print("no data in registry")
        else:
            print("no global registry set")


        print("execute/end: InsertBevyComponent\n")
        # blender uses strings to indicate when operation is done
        return {'FINISHED'}

# ---------------------------------- #
#  Skein Panel for adding components #
# ---------------------------------- #

class SkeinPanel(bpy.types.Panel):
    """Creates a Panel in the Object Properties window"""
    bl_label = "Skein Bevy Panel"
    bl_idname = "OBJECT_PT_skein"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'object'

    def draw(self, context):
        layout = self.layout
        obj = context.object
        obj_skein = obj.skein
        active_component_index = obj.active_component_index
        global_skein = context.window_manager.skein
        # TODO: the registry can likely be loaded into a dict in a less
        # common place. This function runs every draw
        registry = json.loads(global_skein.registry)
        skein_property_groups = context.window_manager.skein_property_groups

        row = layout.row()
        
        row.prop_search(
            context.window_manager,
            'selected_component',
            global_skein,
            "components",
            text="C:"
        )

        row = layout.row()
        row.operator("bevy.insert_bevy_component")

        layout.template_list(
            "UI_UL_list",
            "components list",
            obj,
            "skein",
            obj,
            "active_component_index"
        )


        box = layout.box()
        # obj_skein is an array of component data
        # empty lists are falsey
        if obj_skein:
            active_component_data = obj_skein[active_component_index]

            box.label(text=active_component_data["type_path"], icon='DOT')
            type_path = active_component_data["type_path"]
            registry_component_reflection_data = registry[type_path]
            active_editor = active_component_data
            # Marker component
            if "properties" not in registry_component_reflection_data and registry_component_reflection_data["kind"] == "Struct":
                box.label(text="Marker components have no data to modify")
            # Other components
            build_ui(box, context.window_manager, "active_editor", registry, type_path, skein_property_groups)


# --------------------------------- #
#  Registration and unregistration  #
# --------------------------------- #

# add to the Blender menus
def menu_func(self, context):
    self.layout.operator(FetchBevyTypeRegistry.bl_idname)

def register():
    print("\n--------\nregister")
    # data types that are stored on the window because blender
    # doesn't seem to have any other good way of storing data
    # for quick access.
    bpy.utils.register_class(ComponentTypeData)
    bpy.utils.register_class(ComponentData)
    bpy.utils.register_class(PGSkeinWindowProps)
    bpy.types.WindowManager.skein = bpy.props.PointerProperty(type=PGSkeinWindowProps)

    bpy.types.Object.skein = bpy.props.CollectionProperty(type=ComponentData)
    bpy.types.Object.active_component_index = bpy.props.IntProperty(
        update=update_component_form
    )

    # TODO: move this to common property group for all object, material, mesh, etc extras
    bpy.types.WindowManager.selected_component = bpy.props.StringProperty(
        name="component type path",
        description="The component that will be added if selected",
        update=on_select_new_component
    )
    # skein_property_groups is a dict keyed by component type_path
    # each type_path's value is a PropertyGroup that we can introspect
    # via __annotations__ to build the UI
    bpy.types.WindowManager.skein_property_groups = {}

    # operations
    bpy.utils.register_class(FetchBevyTypeRegistry)
    bpy.utils.register_class(InsertBevyComponent)
    # panel
    bpy.utils.register_class(SkeinPanel)
    # adds the menu_func layout to an existing menu
    bpy.types.TOPBAR_MT_edit.append(menu_func)

    # gltf extension
    bpy.utils.register_class(SkeinExtensionProperties)
    bpy.types.Scene.skein_extension_properties = bpy.props.PointerProperty(type=SkeinExtensionProperties)

    # Use the following 2 lines to register the UI for the gltf extension hook
    from io_scene_gltf2 import exporter_extension_layout_draw
    exporter_extension_layout_draw['Example glTF Extension'] = draw_export # Make sure to use the same name in unregister()
    print("\nregister/end")

def unregister():
    # data types that are stored on the window because blender
    # doesn't seem to have any other good way of storing data
    # for quick access.
    bpy.utils.unregister_class(PGSkeinWindowProps)
    bpy.utils.unregister_class(ComponentTypeData)
    bpy.utils.unregister_class(ComponentData)
    # operations
    bpy.utils.unregister_class(FetchBevyTypeRegistry)
    bpy.utils.unregister_class(InsertBevyComponent)
    # panel
    bpy.utils.unregister_class(SkeinPanel)

    # gltf extension
    bpy.utils.unregister_class(SkeinExtensionProperties)
    del bpy.types.Scene.skein_extension_properties

    # Use the following 2 lines to unregister the UI for this hook
    from io_scene_gltf2 import exporter_extension_layout_draw
    del exporter_extension_layout_draw['Example glTF Extension'] # Make sure to use the same name in register()

# This is for testing, which allows running this script directly from Blender's Text editor
# It enables running this script without installing
if __name__ == "__main__":
    register()


# the registry is the full bevy reflection information
# the component_key is the first key into the registry, "event_ordering::PowerLevel" here:
#
# ```json
#   "event_ordering::PowerLevel": {
#     "additionalProperties": false,
#     "crateName": "event_ordering",
#     "kind": "Struct",
#     "modulePath": "event_ordering",
#     "properties": {
#       "name": {
#         "type": {
#           "$ref": "#/$defs/f32"
#         }
#       }
#     },
#     "reflectTypes": [
#       "Component",
#       "Serialize",
#       "Deserialize"
#     ],
#     "required": [
#       "name"
#     ],
#     "shortPath": "PowerLevel",
#     "type": "object",
#     "typePath": "event_ordering::PowerLevel"
#   },
# ```
def build_ui(layout, context, context_key, registry, type_path, skein_property_groups):
    if type_path in skein_property_groups:
        component_data = skein_property_groups[type_path]
        render_props(layout, context, context_key, component_data)
    else:
        layout.label(text="No property group for " + type_path)

def render_props(layout, context, context_key, component_data):
    # print("\n# render_props", context, context_key)
    # print(context.id_data)
    # print(component_data)
    # print(getattr(context, context_key))
    # print(dir(getattr(context, context_key)))
    # print(getattr(getattr(context, context_key), "bl_rna"))
    # print(">>>")
    if context_key != "active_editor":
        for key,value in getattr(getattr(context, context_key), "__annotations__").items():
            # print("rendering ", key, " with ", value)
            layout.prop(getattr(context, context_key), key)
    # print(">>>")
    # print(inspect.get_annotations(getattr(context, context_key)))
    # print(component_data["type"])
    # print("\n")
    # TODO: match on group type
    # TODO: this may only work for Structs
    # print("component_data", component_data)
    component_fields = inspect.get_annotations(component_data)
    if "skein_enum_index" in component_fields:
        active_enum_variant = getattr(getattr(context, context_key), "skein_enum_index")
        component_fields = {
            "skein_enum_index": component_fields["skein_enum_index"],
            active_enum_variant: component_fields[active_enum_variant]
        }
    # print(component_fields)
    # print("\n")
    if component_fields:
        for key in component_fields:
            # print("  - ", context_key, key)
            # print(registry[type_path])
            # field = getattr(context, context_key)[key]
            
            # if sub-field is a PropertyGroup
            # print("## sub-field: " + key)
            # print(component_fields[key].keywords)
            # print(component_fields[key])
            # print(inspect.get_annotations(component_fields[key]))
            if "PointerProperty" == component_fields[key].function.__name__:
                # print("  - is PointerProperty")
                box = layout
                box.separator(type='LINE')
                box.label(text=key, icon='DOT')
                render_props(box, getattr(context, context_key), key, component_fields[key])
                box.separator(type='LINE')
            else:
                # print("  - not PointerProperty")
                layout.prop(getattr(context, context_key), key)
    else:
        if context_key == "active_editor":
            layout.prop(context, context_key)
        else:
            # print("not rendering something", context, context_key)
            pass



# capitalize a word without lowercasing the result
# of the word. This means TeamMember stays and doesn't
# turn into Teammember
def cap(val):
  return val[0].upper() + val[1:]

def capitalize_path(s):
    return "".join(map(cap, re.split('[:_]+', s)))

def make_property(
        skein_property_groups,
        registry,
        original_type_path,
        override_component=None
):
    """build a subclass of ComponentData or return a "scalar" property
    The subclass is a PropertyGroup that we can build up when we fetch the registry,
    The UI to editor a type is built from these PropertyGroup classes

    @param: skein_property_groups All of the property groups constructed so far. Will mutate this to add more property groups.
    @param: registry dict representation of the Bevy registry information
    @param: original_type_path Either a full type_path (`component_tests::SomeThings::OneThing`) or a type_path with `#/#defs/alloc` on the front
    @param: override_component An optional value that is used when you have access to the registry type information but that registry type information is not directly accessible by registry[type_path]. This happens in complex enums. (default None)
    """

    type_path = original_type_path.removeprefix("#/$defs/")
    component = override_component if override_component != None else registry[type_path]

    if type_path in skein_property_groups:
        # The type was already constructed and can be 
        # returned from the "cache" instead of being
        # created again
        return skein_property_groups[type_path]

    print("\nmake_property::", type_path)

    match component["kind"]:
        case "Array":
            print("Array is unimplemented in make_property")
            return
        case "Enum":
            print("Enum: ", component["type"])
            match component["type"]:
                case "string":
                    items = []
                    for item in component["oneOf"]:
                        items.append((item, item, ""))

                    print(items)

                    # TODO: make an enum default value
                    skein_property_groups[type_path] = bpy.props.EnumProperty(
                        items=items,
                        update=update_component_data
                    )

                    return skein_property_groups[type_path]
                case "object":
                    annotations = {}
                    # print("Enum.object is unimplemented")
                    items = []
                    for item in component["oneOf"]:
                        items.append((item["shortPath"], item["shortPath"], ""))

                    print(items)

                    annotations["skein_enum_index"] = bpy.props.EnumProperty(
                        name="variant",
                        items=items,
                        update=update_component_data
                    )
                                # only recurse if we have properties to set, otherwise
                    # annotations should be an empty object

                    for option in component["oneOf"]:
                        print("- option: ", option["shortPath"])
                        key = option["shortPath"]
                        property = make_property(
                            skein_property_groups,
                            registry,
                            option["typePath"],
                            option
                        )
                        if inspect.isclass(property):
                            annotations[key] = bpy.props.PointerProperty(type=property)
                        else:
                            annotations[key] = property

                    # add this struct type to the skein_property_groups so it 
                    # can be accessed elsewhere by type_path
                    skein_property_groups[type_path] = type(capitalize_path(type_path), (ComponentData,), {
                        '__annotations__': annotations,
                    })

                    # registering the class is required for certain Blender
                    # functionality to work.
                    print("REGISTERING: " + type_path)
                    bpy.utils.register_class(
                        skein_property_groups[type_path]
                    )

                    # return the type we just constructed
                    return skein_property_groups[type_path]
                case _:
                    print("unknown Enum type")
                    return
        case "List":
            print("List is unimplemented in make_property")
            return
        case "Map":
            print("Map is unimplemented in make_property")
            return
        case "Set":
            print("Set is unimplemented in make_property")
            return
        case "Struct":
            annotations = {}
            # only recurse if we have properties to set, otherwise
            # annotations should be an empty object
            if "properties" in component:
                for key in component["properties"]:
                    print("- key: ", key)
                    property = make_property(
                        skein_property_groups,
                        registry,
                        component["properties"][key]["type"]["$ref"]
                    )
                    if inspect.isclass(property):
                        annotations[key] = bpy.props.PointerProperty(type=property)
                    else:
                        annotations[key] = property

            # add this struct type to the skein_property_groups so it 
            # can be accessed elsewhere by type_path
            skein_property_groups[type_path] = type(capitalize_path(type_path), (ComponentData,), {
                '__annotations__': annotations,
            })

            # registering the class is required for certain Blender
            # functionality to work.
            print("REGISTERING: " + type_path)
            bpy.utils.register_class(
                skein_property_groups[type_path]
            )

            # return the type we just constructed
            return skein_property_groups[type_path]
        case "Tuple":
            if len(component["prefixItems"]) == 1:
                skein_property_groups[type_path] = make_property(
                    skein_property_groups,
                    registry,
                    component["prefixItems"][0]["type"]["$ref"]
                )
                return skein_property_groups[type_path]
            else:
                print("Tuple is unimplemented in make_property for lengths longer than 1 element")
                return
        case "TupleStruct":
            # single element tuple struct is a special case
            # because the reflection format treats it as a
            # single value for the type_path key
            # ```
            # { "skein::tests::TupleStruct": 12 }
            # ```
            if len(component["prefixItems"]) == 1:
                skein_property_groups[type_path] = make_property(
                    skein_property_groups,
                    registry,
                    component["prefixItems"][0]["type"]["$ref"]
                )
                return skein_property_groups[type_path]
            else:
                print("TupleStruct is unimplemented in make_property for lengths longer than 1 element")
                return
        case "Value":
            # print("- component[type]:  ", component["type"])
            match component["type"]:
                case "uint":
                    match type_path:
                        case "u8":
                            return bpy.props.IntProperty(
                                min=0,
                                max=255,
                                update=update_component_data
                            )
                        case "u16":
                            return bpy.props.IntProperty(
                                min=0,
                                max=65535,
                                update=update_component_data
                            )
                        case "u32":
                            return bpy.props.IntProperty(
                                min=0,
                                # blender actually sets the default hard maximum to
                                # 2^31, not 2^32, so not sure if we can even set
                                # those numbers from inside blender
                                # max=4294967295,
                                update=update_component_data
                        )
                        case "u64":
                            return bpy.props.IntProperty(
                                min=0,
                                # blender actually sets the default hard maximum to
                                # 2^31, not 2^32, so not sure if we can even set
                                # those numbers from inside blender
                                # max=4294967295,
                                update=update_component_data
                        )
                        case "usize":
                            return bpy.props.IntProperty(
                                min=0,
                                # blender actually sets the default hard maximum to
                                # 2^31, not 2^32, so not sure if we can even set
                                # those numbers from inside blender
                                # max=4294967295,
                                update=update_component_data
                        )
                        case _:
                            print("unknown uint type: ", type_path)
                            return bpy.props.IntProperty(min=0, update=update_component_data)
                case "int":
                    match type_path:
                        case "i8":
                            return bpy.props.IntProperty(
                                min=-128,
                                max=127,
                                update=update_component_data
                            )
                        case "i16":
                            return bpy.props.IntProperty(
                                min=-32_768,
                                max=32_767,
                                update=update_component_data
                            )
                        case "i32":
                            return bpy.props.IntProperty(
                                min=-2_147_483_648,
                                max=2_147_483_647,
                                update=update_component_data
                        )
                        case "i64":
                            return bpy.props.IntProperty(update=update_component_data)
                        case "isize":
                            return bpy.props.IntProperty(update=update_component_data)
                        case _:
                            print("unknown iint type: ", type_path)
                            return bpy.props.IntProperty(min=0, update=update_component_data)
                case "float":
                    return bpy.props.FloatProperty(update=update_component_data)
                case "string":
                    return bpy.props.StringProperty(update=update_component_data)
                case "object":
                    match component["type_path"]:
                        case "core::time::Duration":
                            print("core::time::Duration is currently not handled")
                            return
                        case _:
                            print("unhandled `Value` of `object` type: ", component["type_path"])
                            return
                case _:
                    print("unhandled type: ", component["type"])
                    return
        # If an exact match is not confirmed, this last case will be used if provided
        case _:
            print("unhandled kind:", component["kind"])
            return "Something's wrong with the world"
