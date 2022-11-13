from datetime import datetime
from beanie import Document, Link
from pydantic import BaseModel
from typing import Optional, List, Union


class ItemRequirements(Document):
    item_id: str
    name: str
    type: str
    comment: str
    status: str
    creation_date: datetime
    last_update: datetime

    class Settings:
        name = "item_requirements"
