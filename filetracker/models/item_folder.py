from pydantic import BaseModel, Field
from .pyobjectid import PyObjectId
from bson import ObjectId
from typing import Optional, List


class ItemFolder(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    project_id: PyObjectId
    order: int
    status: int
    item_type: str = "folder"
    parent: Optional[PyObjectId]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
                "example": {
                    "name": "My Item Folder",
                    "project_id": "1923801231023",
                    "order": "0",
                    "status": "0"
                    }
                }
