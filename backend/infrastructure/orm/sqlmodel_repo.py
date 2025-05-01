from sqlmodel import Session, select
from typing import List, Optional
from app.domain.models import Item, ItemDomain
from app.interfaces.repositories import ItemRepository

class SQLModelItemRepository(ItemRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[Item]:
        statement = select(Item)
        return self.session.exec(statement).all()
    
    def find_by_id(self, item_id: int) -> Optional[Item]:
        return self.session.get(Item, item_id)
    
    def save(self, item: Item) -> Item:
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item
    
    def remove(self, item_id: int) -> None:
        item = self.find_by_id(item_id)
        if item:
            self.session.delete(item)
            self.session.commit()
    
    def find_by_name(self, name: str) -> List[Item]:
        statement = select(Item).where(Item.name.contains(name))
        return self.session.exec(statement).all()

# Funciones auxiliares para mapear entre el modelo de dominio y el modelo del ORM
def to_domain(item: Item) -> ItemDomain:
    return ItemDomain(id=item.id, name=item.name, description=item.description)

def to_orm(item_domain: ItemDomain) -> Item:
    return Item(id=item_domain.id, name=item_domain.name, description=item_domain.description)
