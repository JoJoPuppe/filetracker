from datetime import datetime
from pydantic import BaseModel, Field
from .pyobjectid import PyObjectId
from bson import ObjectId
from typing import Optional, List


class ProjectHome(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    creation_date: datetime = datetime.now()
    items: Optional[List[PyObjectId]]

    class Config:
            allow_population_by_field_name = True
            arbitrary_types_allowed = True
            json_encoders = {ObjectId: str}
            schema_extra = {
                "example": {
                    "name": "Test Project"
                }
            }
