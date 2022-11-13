from datetime import datetime
from beanie import Document, Link
from pydantic import BaseModel
from typing import Optional, List, Union




class ItemHistory(Document):
    item_id: str
    name: str
    path: str
    comment: str

    class Settings:
        name = "item_history"


