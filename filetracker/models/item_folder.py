from pydantic import BaseModel, Field
from .pyobjectid import PyObjectId
from bson import ObjectId
from typing import Optional, List
import uuid as uuid_pkg


class ItemFolder(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    project_id: PyObjectId
    order: int = 0
    status: int
    item_type: str = "folder"
    item_id: uuid_pkg.UUID = Field(default_factory=uuid_pkg.uuid4)
    parent: Optional[PyObjectId]
    children: List = []

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
                "example": {
                    "name": "My Item Folder",
                    "project_id": "1923801231023",
                    "status": "0"
                    }
                }
