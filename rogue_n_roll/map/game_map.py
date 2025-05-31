from typing import List, Optional, Set, Tuple, TYPE_CHECKING
import numpy as np
import tcod
from tcod import libtcodpy

if TYPE_CHECKING:
    from ..game_objects.entity import Entity
    from ..game_objects.item import Item


class GameMap:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.tiles = np.full((height, width), fill_value=False, dtype=bool)  # True означает проходимый тайл
        self.explored = np.full((height, width), fill_value=False, dtype=bool)
        self.visible = np.full((height, width), fill_value=False, dtype=bool)
        self.entities: List[Entity] = []
        self.items: List[Item] = []

    def in_bounds(self, x: int, y: int) -> bool:
        """Проверяет, находятся ли координаты в пределах карты."""
        return 0 <= x < self.width and 0 <= y < self.height

    def is_walkable(self, x: int, y: int) -> bool:
        """Проверяет, можно ли пройти через указанную клетку."""
        if not self.in_bounds(x, y):
            return False
        if not self.tiles[y, x]:  # Обратите внимание на порядок индексов [y, x]
            return False
        return not any(entity.is_blocking and entity.x == x and entity.y == y for entity in self.entities)

    def get_blocking_entity_at(self, x: int, y: int) -> Optional["Entity"]:
        """Возвращает блокирующую сущность в указанной позиции."""
        for entity in self.entities:
            if entity.is_blocking and entity.x == x and entity.y == y:
                return entity
        return None

    def get_items_at(self, x: int, y: int) -> List["Item"]:
        """Возвращает список предметов в указанной позиции."""
        return [item for item in self.items if item.x == x and item.y == y]

    def update_fov(self, player_x: int, player_y: int, radius: int) -> None:
        """Обновляет поле зрения."""
        # Создаем карту прозрачности: True для проходимых клеток, False для стен
        transparency = np.array(self.tiles, dtype=bool)
        
        # Вычисляем поле зрения
        self.visible = tcod.map.compute_fov(
            transparency=transparency,
            pov=(player_y, player_x),
            radius=radius,
            light_walls=True,
            algorithm=libtcodpy.FOV_SYMMETRIC_SHADOWCAST,
        )
        
        # Обновляем исследованные клетки
        self.explored |= self.visible

    def add_entity(self, entity: "Entity") -> None:
        """Добавляет сущность на карту."""
        self.entities.append(entity)
        entity.game_map = self

    def remove_entity(self, entity: "Entity") -> None:
        """Удаляет сущность с карты."""
        if entity in self.entities:
            self.entities.remove(entity)
            entity.game_map = None

    def add_item(self, item: "Item") -> None:
        """Добавляет предмет на карту."""
        self.items.append(item)
        item.game_map = self

    def remove_item(self, item: "Item") -> None:
        """Удаляет предмет с карты."""
        if item in self.items:
            self.items.remove(item)
            item.game_map = None 