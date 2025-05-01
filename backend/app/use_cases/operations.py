from app.interfaces.repositories import ItemRepository

def list_items(repo: ItemRepository):
    return repo.get_all()
