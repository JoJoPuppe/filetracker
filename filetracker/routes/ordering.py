from beanie import Document, Link
from pydantic import BaseModel
from typing import Optional, List, Union

class Ordering(Document):
    project_id: str
    folder_order: str

    class Settings:
        name = "ordering"
