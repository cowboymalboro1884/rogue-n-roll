from typing import Optional, Tuple, TYPE_CHECKING
from rogue_n_roll.game_objects.game_object import GameObject

if TYPE_CHECKING:
    from rogue_n_roll.game_objects.entity import Entity


class Item(GameObject):
    def __init__(
        self,
        x: int,
        y: int,
        char: str,
        color: Tuple[int, int, int],
        name: str,
        description: str,
        is_blocking: bool = False,
    ):
        super().__init__(x, y, char, color, name, is_blocking=is_blocking)
        self.description = description

    def use(self, user: "Entity") -> bool:
        """Использует предмет. Возвращает True, если предмет нужно удалить из инвентаря."""
        return False

    def pick_up(self, user: "Entity") -> bool:
        """Подбирает предмет. Возвращает True, если успешно."""
        if user.inventory.add_item(self):
            if self.game_map:
                self.game_map.remove_item(self)
            return True
        return False

    def drop(self, user: "Entity") -> bool:
        """Выбрасывает предмет. Возвращает True, если успешно."""
        if user.game_map and user.inventory.remove_item(self):
            self.x = user.x
            self.y = user.y
            user.game_map.add_item(self)
            return True
        return False 