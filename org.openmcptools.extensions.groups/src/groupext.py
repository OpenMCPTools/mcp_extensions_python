from mcp.types import BaseMetadata

from typing import Any, Self
from pydantic import ConfigDict, Field

class Group(BaseMetadata):
    
    description: str | None = None

    parent: Self | None = None

    meta: dict[str, Any] | None = Field(alias="_meta", default=None)

    model_config = ConfigDict(extra="allow")
    
    def _get_parent_name(self, sb: str, tg: Self, separator: str) -> str:
        return self._get_parent_name(sb, self.parent, separator) + separator + tg.name if tg.parent else tg.name

    def get_fully_qualified_name(self, name_separator: str = ".") -> str:
        return self._get_parent_name("", self, name_separator)
