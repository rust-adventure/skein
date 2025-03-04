skein is split into two pieces:

- Rust crate (Bevy Plugin)
- Blender Addon (Python)

## Rust crate

The Rust crate is a Bevy plugin. Nothing special, just a Cargo.toml. `cargo test`, etc all work.

## Blender Addon

The Blender addon is written in Python and comes with the usual python requirements.

`__init__.py` is written in such a way that you can copy/paste the file into the a new scripting text file in the Blender Scripting tab, then run it. You don't have to install anything if you do this, but you won't be able to run tests.

## Testing

For more automated testing, I happen to be using [pipx](https://github.com/pypa/pipx) and [virtualenv](https://virtualenv.pypa.io), and [pyenv]()

```
brew install pipx pyenv
pipx ensurepath
pipx install virtualenv
pyenv install 3.10
# pyenv shims will show you the path to a python 3.10, which is
# required for bpy to install
pyenv shims
virtualenv skein-dev -p /Users/chris/.pyenv/shims/python3.10
source skein-dev/bin/activate
pip install bpy requests
pip install -U pytest
```

## The Python Dataflow

#### WindowManager

- registry
  - holds the json registry data as a string from the brp request
- components
  - a Collection of component data used for creating lists the user can select a component from
- skein_property_groups
  - The property groups created after fetching the registry data

#### Object

- skein
  - Collection of component data

##### ComponentData

- type_path
- name
- value
