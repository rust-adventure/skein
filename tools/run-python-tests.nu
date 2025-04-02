# This runs the Blender Python export tests
# it checks against the combined snapshot files to 
# make sure that we're producing the serialized 
# data format that Bevy will accept.

def main [] {
    blender --background --factory-startup --python tools/blender_python_embedded_tests.py  -- --verbose
}

