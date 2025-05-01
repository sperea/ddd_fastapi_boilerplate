from sqlmodel import Session, select
from typing import List
from app.domain.models import Item, ItemDomain
from app.interfaces.repositories import ItemRepository
from app.infrastructure.database import Item

class SQLModelItemRepository(ItemRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[Item]:
        statement = select(Item)
        return self.session.exec(statement).all()

# Implementa una función para mapear entre el modelo de dominio y el modelo del ORM
def to_domain(item: Item) -> ItemDomain:
    return ItemDomain(id=item.id, name=item.name, description=item.description)

def to_orm(item_domain: ItemDomain) -> Item:
    return Item(id=item_domain.id, name=item_domain.name, description=item_domain.description)
