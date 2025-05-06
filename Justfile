# It is notable that Blender seems unable to select the latest version
# if multiple versions are present (ex: if someone has 0.1.6 installed and
# 0.1.6 and 0.1.7 are *both* in the releases folder/index, then Blender 
# will just repeatedly re-install 0.1.6... which does nothing for the user.
#
# run blender headless to generate the static extension registry index
generate-static-index:
    blender --command extension server-generate --repo-dir=./assets/releases