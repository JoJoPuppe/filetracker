from datetime import datetime
from pydantic import BaseModel, Field
from .pyobjectid import PyObjectId
from bson import ObjectId
from typing import Optional, List


class ItemLog(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    creation_date: datetime = Field(...)
    last_update: datetime = Field(...)
    log_message: str = Field(...)
    project_id: PyObjectId

    class Config:
            allow_population_by_field_name = True
            arbitrary_types_allowed = True
            json_encoders = {ObjectId: str}
            schema_extra = {
                "example": {
                    "log_message": "<h1>Hello</h1>"
                }
            }
