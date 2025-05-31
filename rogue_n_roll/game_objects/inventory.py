from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from rogue_n_roll.game_objects.item import Item


class Inventory:
    def __init__(self, capacity: int = 26):  # По умолчанию 26 слотов (по буквам алфавита)
        self.capacity = capacity
        self.items: List["Item"] = []

    def add_item(self, item: "Item") -> bool:
        """Добавляет предмет в инвентарь. Возвращает True, если успешно."""
        if len(self.items) >= self.capacity:
            return False
        self.items.append(item)
        return True

    def remove_item(self, item: "Item") -> bool:
        """Удаляет предмет из инвентаря. Возвращает True, если успешно."""
        if item in self.items:
            self.items.remove(item)
            return True
        return False

    def get_item(self, index: int) -> Optional["Item"]:
        """Возвращает предмет по индексу."""
        if 0 <= index < len(self.items):
            return self.items[index]
        return None

    def is_full(self) -> bool:
        """Проверяет, заполнен ли инвентарь."""
        return len(self.items) >= self.capacity 