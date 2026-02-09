from mcp.types import BaseMetadata

from typing import Any, Self
from pydantic import ConfigDict, Field

class Group(BaseMetadata):
    
    description: str | None = None

    parent: Self | None = None

    meta: dict[str, Any] | None = Field(alias="_meta", default=None)

    model_config = ConfigDict(extra="allow")