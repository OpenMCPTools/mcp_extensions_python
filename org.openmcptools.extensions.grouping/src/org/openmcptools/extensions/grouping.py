from pydantic import ConfigDict, Field

from typing import Any, Self
from mcp.types import BaseMetadata

EXTENSION_ID = "org.openmcptools/grouping"
    
class GroupSchema(BaseMetadata):
    '''schema for group extension.  Inherit name, title from BaseMetadata'''
    description: str | None = None
    '''description for the GroupExtension type'''
    parent: Self | None = None
    '''Optional parent to allow for hierarchical grouping'''
    meta: dict[str, Any] | None = Field(alias="_meta", default=None)
    '''standard meta object for GroupExtension type'''
    model_config = ConfigDict(extra="allow")

