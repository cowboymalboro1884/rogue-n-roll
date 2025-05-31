from typing import Optional, Tuple, TYPE_CHECKING
from rogue_n_roll.game_objects.game_object import GameObject
from rogue_n_roll.game_objects.stats import Stats
from rogue_n_roll.game_objects.inventory import Inventory

if TYPE_CHECKING:
    from rogue_n_roll.map.game_map import GameMap
    from rogue_n_roll.game_objects.item import Item


class Entity(GameObject):
    def __init__(
        self,
        x: int,
        y: int,
        char: str,
        color: Tuple[int, int, int],
        name: str,
        stats: Optional[Stats] = None,
        is_blocking: bool = True,
    ):
        super().__init__(x, y, char, color, name, is_blocking=is_blocking)
        self.stats = stats or Stats()
        self.inventory = Inventory()

    def move(self, dx: int, dy: int) -> None:
        """Перемещает сущность."""
        self.x += dx
        self.y += dy

    def attack(self, target: "Entity") -> None:
        """Атакует другую сущность."""
        damage = max(0, self.stats.attack_power - target.stats.defense)
        target.stats.take_damage(damage)

    def is_alive(self) -> bool:
        """Проверяет, жива ли сущность."""
        return self.stats.current_hp > 0

    def pick_up_item(self, item: "Item") -> bool:
        """Подбирает предмет с земли."""
        return item.pick_up(self)

    def drop_item(self, item: "Item") -> bool:
        """Выбрасывает предмет на землю."""
        return item.drop(self)

    def use_item(self, item: "Item") -> bool:
        """Использует предмет из инвентаря."""
        if item not in self.inventory.items:
            return False
        if item.use(self):
            self.inventory.remove_item(item)
        return True

    def distance_to(self, other: GameObject) -> float:
        """Вычисляет расстояние до другого объекта."""
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def move_towards(self, target_x: int, target_y: int) -> None:
        """Перемещает сущность в направлении целевой точки."""
        dx = target_x - self.x
        dy = target_y - self.y
        distance = max(abs(dx), abs(dy))

        if distance > 0:
            dx = int(round(dx / distance))
            dy = int(round(dy / distance))
            self.move(dx, dy)

    def take_damage(self, amount: int) -> None:
        """Наносит урон сущности."""
        self.stats.take_damage(amount)

    def heal(self, amount: int) -> None:
        """Восстанавливает здоровье сущности."""
        self.stats.heal(amount) 