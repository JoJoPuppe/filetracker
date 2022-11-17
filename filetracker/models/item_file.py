from datetime import datetime
from pydantic import BaseModel, Field
from .pyobjectid import PyObjectId
from bson import ObjectId
from typing import Optional, List


class ItemFile(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    item_type: str = "file"
    path: str
    name: str
    file_name: str
    status: int
    project_id: PyObjectId
    file_type: str
    creation_date: datetime
    last_update: datetime = datetime.now()
    operator: str
    comment: str
    parent: Optional[PyObjectId]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
                "example": {
                    "path": "/new/path/to/file",
                    "name": "My Item File",
                    "file_name": "221022_my_item_file.ext",
                    "status": "0",
                    "project_id": "1923801231023",
                    "file_type": "text",
                    "creation_date": "2008-09-15T15:57:00+05:00",
                    "operator": "jojo",
                    "comment": "this is a new item"
                    }
                }
