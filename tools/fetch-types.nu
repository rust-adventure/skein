http post --content-type application/json http://127.0.0.1:15702 {"jsonrpc": "2.0", "method": "bevy/registry/schema", "params": {}} | get result | to json | save registry.json