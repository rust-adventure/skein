# validate the source code for the blender extension
validate:
    Blender --command extension validate extension/
# validate the produced .zip file with the blender extension in it
validate-zip:
    Blender --command extension validate bevy_skein-*.zip
# build the blender extension
build:
    Blender --command extension build --source-dir extension/

doc:
    cargo doc --all-features --no-deps --document-private-items
clippy:
    cargo clippy

copy-for-dev:
    cp -r ./extension/* /Users/chris/Library/Application\ Support/Blender/4.2/extensions/user_default/bevy_skein 