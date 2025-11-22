# validate the source code for the blender extension
validate:
    Blender --command extension validate extension/
# validate the produced .zip file with the blender extension in it
validate-zip:
    Blender --command extension validate bevy_skein-*.zip
# build the blender extension
build:
    Blender --command extension build --source-dir extension/
# document the rust crate
doc:
    cargo doc --all-features --no-deps --document-private-items
clippy:
    cargo clippy

# copy-for-dev is a mac-specific filepath located to a directory
# on my own (chris') filesystem. You'll want to change this path if
# you're working on a different OS or with a different Blender version
# requires a Blender restart.
#
# copies the python extension directly into the Blender addons directory.
copy-for-dev:
    cp -r ./extension/* /Users/chris/Library/Application\ Support/Blender/5.0/extensions/user_default/bevy_skein/

# run python tests headlessly in a blender environment
run-headless-blender-tests:
    nu ./tools/run-python-tests.nu

# combine all test-components/snapshots into one json file
gather-snapshots:
    nu ./tools/gather-snapshots.nu