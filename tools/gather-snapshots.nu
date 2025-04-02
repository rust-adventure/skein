# Open all the snapshot files and write it to a new, combined file.
# This gives us a base on which to use the serialized data and check
# it against the python serialization from the blender addon
open test-components/src/snapshots/*.snap | each {|e| $e | split row "---" | last | from json } | to json | save combined_snapshots.json