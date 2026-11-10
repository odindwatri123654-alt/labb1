"""Слой хранения: один простой репозиторий для любых наших объектов."""


class Repository:
    def __init__(self):
        self.items = {}
        self.next_id = 1

    def add(self, item):
        item.id = self.next_id
        self.items[item.id] = item
        self.next_id += 1
        return item

    def get(self, item_id):
        if item_id not in self.items:
            raise ValueError("Объект с таким номером не найден.")
        return self.items[item_id]

    def get_all(self):
        return list(self.items.values())

    def update(self, item):
        self.get(item.id)
        self.items[item.id] = item

    def delete(self, item_id):
        self.get(item_id)
        del self.items[item_id]
