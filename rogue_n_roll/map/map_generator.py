from typing import List, Tuple
import random
import tcod
import numpy as np
from .game_map import GameMap
from rogue_n_roll.game_objects.items import HealthPotion, Sword, Shield, ScrollOfLightning


class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def center(self) -> Tuple[int, int]:
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2
        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Возвращает внутреннюю область комнаты."""
        return slice(self.y1 + 1, self.y2), slice(self.x1 + 1, self.x2)

    def intersects(self, other: "RectangularRoom") -> bool:
        """Возвращает True если эта комната пересекается с другой."""
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )


class MapGenerator:
    def __init__(
        self,
        map_width: int,
        map_height: int,
        room_min_size: int = 6,
        room_max_size: int = 10,
        max_rooms: int = 30,
    ):
        self.map_width = map_width
        self.map_height = map_height
        self.room_min_size = room_min_size
        self.room_max_size = room_max_size
        self.max_rooms = max_rooms
        self.game_map = GameMap(map_width, map_height)

    def _create_room(self, game_map: GameMap, room: RectangularRoom) -> None:
        """Создает проходимую комнату."""
        game_map.tiles[room.inner] = True

    def _create_horizontal_tunnel(
        self, game_map: GameMap, x1: int, x2: int, y: int
    ) -> None:
        """Создает горизонтальный туннель."""
        x1, x2 = min(x1, x2), max(x1, x2)
        game_map.tiles[y, x1 : x2 + 1] = True

    def _create_vertical_tunnel(
        self, game_map: GameMap, y1: int, y2: int, x: int
    ) -> None:
        """Создает вертикальный туннель."""
        y1, y2 = min(y1, y2), max(y1, y2)
        game_map.tiles[y1 : y2 + 1, x] = True

    def generate_map(self) -> Tuple[GameMap, List[RectangularRoom]]:
        """Генерирует новую карту подземелья."""
        rooms: List[RectangularRoom] = []

        for _ in range(self.max_rooms):
            room_width = random.randint(self.room_min_size, self.room_max_size)
            room_height = random.randint(self.room_min_size, self.room_max_size)

            x = random.randint(0, self.map_width - room_width - 1)
            y = random.randint(0, self.map_height - room_height - 1)

            new_room = RectangularRoom(x, y, room_width, room_height)

            if any(new_room.intersects(other_room) for other_room in rooms):
                continue

            self._create_room(self.game_map, new_room)

            if rooms:
                prev_x, prev_y = rooms[-1].center
                new_x, new_y = new_room.center

                if random.random() < 0.5:
                    self._create_horizontal_tunnel(self.game_map, prev_x, new_x, prev_y)
                    self._create_vertical_tunnel(self.game_map, prev_y, new_y, new_x)
                else:
                    self._create_vertical_tunnel(self.game_map, prev_y, new_y, prev_x)
                    self._create_horizontal_tunnel(self.game_map, prev_x, new_x, new_y)

            # Добавляем предметы в комнату
            self._place_items(new_room)

            rooms.append(new_room)

        return self.game_map, rooms

    def _place_items(self, room: RectangularRoom) -> None:
        """Размещает предметы в комнате."""
        # Шанс появления предметов
        if random.random() < 0.7:  # 70% шанс появления предмета в комнате
            # Выбираем случайную позицию в комнате
            x = random.randint(room.x1 + 1, room.x2 - 1)
            y = random.randint(room.y1 + 1, room.y2 - 1)

            # Выбираем случайный предмет
            item_class = random.choice([
                HealthPotion,
                Sword,
                Shield,
                ScrollOfLightning
            ])

            # Создаем и добавляем предмет
            item = item_class(x, y)
            self.game_map.add_item(item) 