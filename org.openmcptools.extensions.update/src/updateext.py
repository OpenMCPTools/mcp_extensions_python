from __future__ import annotations
from enum import Enum
from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field, ConfigDict

# Translated from PrimitiveUpdateConfig.java
class PrimitiveUpdateConfig:
    """
    Configuration constants for the primitive update extension.
    """
    EXTENSION_ID: str = "org.openmcptools/update"

    SERVER_CAPABILITIES_ID: str = EXTENSION_ID + "/server"
    CLIENT_CAPABILITIES_ID: str = EXTENSION_ID + "/client"

    NOTIFICATION_TOPIC: str = "notification/tools/updated"

    # Note: Typo "primtive" preserved from original Java source
    PRIMITIVE_UPDATE_EVENTS_KEY: str = "primtiveUpdateEvents"


class FieldValueUpdate(BaseModel):
    """
    Represents a value update for a specific field, including revision and version tracking.
    """
    model_config = ConfigDict(
        populate_by_name=True,
        extra='ignore',
    )

    previous: Optional[FieldValueUpdate] = Field(default=None, alias="previous")

    fieldName: Optional[str] = Field(default=None, alias="fieldName")

    fieldValue: Optional[Any] = Field(default=None, alias="fieldValue")

    createRevision: Optional[int] = Field(default=None, alias="createRevision")

    modRevision: Optional[int] = Field(default=None, alias="modRevision")

    version: Optional[int] = Field(default=None, alias="version")

    lease: Optional[int] = Field(default=None, alias="lease")

    @staticmethod
    def convertToLong(o: Any) -> int:
        """
        Mimics Java's logic of converting an object to a Long (int in Python), 
        returning 0 if the object is not a numeric type.
        """
        if isinstance(o, int):
            return o
        elif isinstance(o, float):
            return int(o)
        return 0

    @classmethod
    def fromMap(cls, data: Dict[str, Any]) -> Optional[FieldValueUpdate]:
        """
        Creates a FieldValueUpdate instance from a dictionary (Map).
        """
        if data is None:
            return None
        
        # Create a new instance
        r = cls.model_construct()
        
        r.fieldName = data.get("fieldName")
        if r.fieldName is None:
            raise ValueError("fieldName must not be null")
            
        r.lease = cls.convertToLong(data.get("lease"))
        r.version = cls.convertToLong(data.get("version"))
        r.modRevision = cls.convertToLong(data.get("modRevision"))
        r.createRevision = cls.convertToLong(data.get("createRevision"))
        r.fieldValue = data.get("fieldValue")
        
        # Recursive call for the 'previous' field
        r.previous = FieldValueUpdate.fromMap(data.get("previous"))
        
        return r


class PrimitiveUpdateEvent(BaseModel):
    """
    Event representing an update (PUT or DELETE) to a primitive.
    """
    model_config = ConfigDict(
        populate_by_name=True,
        extra='ignore',
    )

    class EventType(str, Enum):
        """
        Enum for the type of event.
        """
        # @JsonProperty("PUT")
        PUT = "PUT"
        # @JsonProperty("DELETE")
        DELETE = "DELETE"

    eventType: Optional[EventType] = Field(default=None, alias="eventType")

    primitiveName: Optional[str] = Field(default=None, alias="primitiveName")

    fieldValueUpdates: Optional[List[FieldValueUpdate]] = Field(default=None, alias="fieldValueUpdates")

    @classmethod
    def fromMap(cls, data: Dict[str, Any]) -> Optional[PrimitiveUpdateEvent]:
        """
        Creates a PrimitiveUpdateEvent instance from a dictionary (Map).
        """
        if data is None:
            return None
            
        r = cls.model_construct()
        
        r.primitiveName = data.get("primitiveName")
        # Replicating Objects.requireNonNull(r.primitiveName, "primitiveName must not be null");
        if r.primitiveName is None:
            raise ValueError("primitiveName must not be null")
            
        event_type_str = data.get("eventType")
        # In Java: r.eventType = eventType.equals("PUT") ? EventType.PUT : EventType.DELETE;
        # Replicating logic where a null eventType in the map would cause an NPE in Java.
        if event_type_str is None:
            raise ValueError("eventType must not be null")
        
        r.eventType = cls.EventType.PUT if event_type_str == "PUT" else cls.EventType.DELETE
        
        list_map = data.get("fieldValueUpdates")
        if list_map is not None:
            # Replicating stream/map/collect logic
            r.fieldValueUpdates = [FieldValueUpdate.fromMap(m) for m in list_map]
            
        return r
