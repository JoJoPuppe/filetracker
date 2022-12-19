from datetime import datetime
from beanie import Document, Link
from pydantic import BaseModel
from typing import Optional, List, Union, Dict
from bson import ObjectId
from pydantic import BaseModel, Field


class ItemRequirements(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    item_id: str
    check_list: Optional(List(Dict))
    creation_date: datetime = datetime.now()

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "item_id": "1231-123-123"
            }
        }
