# MCP Extensions — Python

Extensions for the MCP (Model Context Protocol) Python SDK.

## Server-Side Grouping

The [org.openmcptools.extensions.groups](https://github.com/OpenMCPTools/mcp_extensions_python/tree/main/org.openmcptools.extensions.groups) module provides an MCP extension to support hierarchical server-side grouping based upon the [python sdk](https://github.com/modelcontextprotocol/python-sdk).

### What's in here

The project defines a tree-based data model to organize **tools**, **prompts**, and **resources** into **hierarchical groups** — like folders inside folders.

#### [Core model](https://github.com/OpenMCPTools/mcp_extensions_python/blob/main/org.openmcptools.extensions.groups/src/common.py) (`src/common.py`)

- **Group** — a tree node. Can contain other groups, tools, prompts, and resources. Each group knows its parent and computes its fully qualified name (e.g. `com.example.api`).
- **Tool** — an MCP tool. Can belong to multiple groups at once.
- **Prompt** — an MCP prompt with typed arguments.
- **Resource** — an MCP resource (URI, size, MIME type).
- **Converter** — generic interface to convert between the internal model and any external format.

#### [Config and Schema/Pydantic Model](https://github.com/OpenMCPTools/mcp_extensions_python/blob/main/org.openmcptools.extensions.groups/src/groupext.py) (`src/groupext.py`)

Extension identifier constants (`org.openmcptools/groups`) and the [pydantic model definition for the Group type and all the common types](https://github.com/OpenMCPTools/mcp_extensions_python/blob/main/org.openmcptools.extensions.groups/src/groupext.py).

#### Schema

The python pydantic model implementation is based upon this json-schema

```json
        "Group": {
            "properties": {
                "name": {
                    "type": "string"
                },
                "parent": {
                    "$ref": "#/definitions/Group",
                },
                "description": {
                    "type": "string"
                },
                "title": {
                    "type": "string"
                },
                "_meta": {
                    "additionalProperties": {},
                    "type": "object"
                }
            },
            "required": [
                "name"
            ],
            "type": "object"
        }
```
This schema for hierarchical grouping was [initially proposed as a MCP protocol enhancement](https://github.com/modelcontextprotocol/modelcontextprotocol/discussions/1567#discussioncomment-14608597).  For a discussion specifically of the 'parent' field, and it's role in hierarchical grouping, [please see this and subsequent postings](https://github.com/modelcontextprotocol/modelcontextprotocol/discussions/1567#discussioncomment-14618688).

The same schema is used for the [mcp_extensions_java group extension](https://github.com/OpenMCPTools/mcp_extensions_java) (Java SDK Extension) and the [mcp_extensions_typescript group extension](https://github.com/OpenMCPTools/mcp_extensions_typescript) (Typescript SDK Extension)
