from sqlmodel import SQLModel, Field
from typing import Optional

class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None

# Define un modelo de dominio puro para Item
class ItemDomain:
    def __init__(self, id: Optional[int], name: str, description: Optional[str] = None):
        self.id = id
        self.name = name
        self.description = description
