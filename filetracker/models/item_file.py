from datetime import datetime
from typing import List, Optional
import uuid as uuid_pkg

from bson import ObjectId
from pydantic import BaseModel, Field

from .pyobjectid import PyObjectId


class ItemFile(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    item_type: str = "file"
    path: str
    name: str
    status: int
    project_id: PyObjectId
    file_type: str
    reject_text: str = ''
    creation_date: datetime = Field(...)
    last_update: datetime = Field(...)
    operator: str
    order_index: int = 0
    comment: str
    link: str
    version: int = 0
    item_id: uuid_pkg.UUID = Field(default_factory=uuid_pkg.uuid4)
    parent: Optional[PyObjectId]
    history: Optional[List[PyObjectId]]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "path": "/new/path/to/file",
                "name": "My Item File",
                "status": "0",
                "project_id": "1923801231023",
                "file_type": "text",
                "operator": "jojo",
                "reject_text": "used wrong Logo file",
                "comment": "this is a new item",
                "link": "http://link.to/asset.mov"
            }
        }
