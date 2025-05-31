from typing import Optional, Set, Tuple, List
import tcod
import tcod.event
import os
import numpy as np
from rogue_n_roll.game_objects.player import Player
from rogue_n_roll.game_objects.monster import Monster
from rogue_n_roll.map.game_map import GameMap
from rogue_n_roll.map.map_generator import MapGenerator
from rogue_n_roll.engine.colors import *


class GameEngine:
    def __init__(self):
        self.screen_width = 80
        self.screen_height = 50
        self.map_width = 80
        self.map_height = 43

        # Состояние интерфейса
        self.show_inventory = False
        self.selected_item_index = 0

        # Создаем консоль
        self.console = tcod.console.Console(self.screen_width, self.screen_height, order="F")
        self.context = None

        # Создаем карту
        map_generator = MapGenerator(self.map_width, self.map_height)
        self.game_map, rooms = map_generator.generate_map()

        # Создаем игрока в центре первой комнаты
        player_x, player_y = rooms[0].center
        self.player = Player(x=player_x, y=player_y)
        self.game_map.add_entity(self.player)

        # Добавляем монстров в другие комнаты
        for room in rooms[1:]:
            if not self.game_map.get_blocking_entity_at(*room.center):
                if len(self.game_map.entities) % 3 == 0:
                    monster = Monster.create_troll(*room.center)
                elif len(self.game_map.entities) % 2 == 0:
                    monster = Monster.create_orc(*room.center)
                else:
                    monster = Monster.create_rat(*room.center)
                self.game_map.add_entity(monster)

    def initialize(self) -> None:
        """Инициализирует игру."""
        tileset = tcod.tileset.load_tilesheet(
            "resources/dejavu10x10_gs_tc.png",
            32,
            8,
            tcod.tileset.CHARMAP_TCOD
        )

        self.context = tcod.context.new(
            columns=self.console.width,
            rows=self.console.height,
            tileset=tileset,
            title="Rogue'n'Roll",
            vsync=True,
        )

    def render_inventory(self) -> None:
        """Отрисовывает инвентарь."""
        inventory_width = 40
        inventory_height = 30
        x = (self.screen_width - inventory_width) // 2
        y = (self.screen_height - inventory_height) // 2

        # Рисуем фон
        for i in range(inventory_height):
            for j in range(inventory_width):
                self.console.print(
                    x=x + j,
                    y=y + i,
                    string=" ",
                    bg=UI_BACKGROUND
                )

        # Рисуем рамку
        for i in range(inventory_width):
            self.console.print(x=x + i, y=y, string="═", fg=UI_KEYS, bg=UI_BACKGROUND)
            self.console.print(x=x + i, y=y + inventory_height - 1, string="═", fg=UI_KEYS, bg=UI_BACKGROUND)
        for i in range(inventory_height):
            self.console.print(x=x, y=y + i, string="║", fg=UI_KEYS, bg=UI_BACKGROUND)
            self.console.print(x=x + inventory_width - 1, y=y + i, string="║", fg=UI_KEYS, bg=UI_BACKGROUND)
        
        # Углы рамки
        self.console.print(x=x, y=y, string="╔", fg=UI_KEYS, bg=UI_BACKGROUND)
        self.console.print(x=x + inventory_width - 1, y=y, string="╗", fg=UI_KEYS, bg=UI_BACKGROUND)
        self.console.print(x=x, y=y + inventory_height - 1, string="╚", fg=UI_KEYS, bg=UI_BACKGROUND)
        self.console.print(x=x + inventory_width - 1, y=y + inventory_height - 1, string="╝", fg=UI_KEYS, bg=UI_BACKGROUND)

        # Заголовок
        self.console.print(
            x=x + (inventory_width - len("INVENTORY")) // 2,
            y=y + 1,
            string="INVENTORY",
            fg=UI_TEXT,
            bg=UI_BACKGROUND
        )

        # Список предметов
        for i, item in enumerate(self.player.inventory.items):
            color = UI_KEYS if i == self.selected_item_index else UI_REGULAR_TEXT
            self.console.print(
                x=x + 2,
                y=y + 3 + i,
                string=f"{chr(97 + i)}) {item.name}",
                fg=color,
                bg=UI_BACKGROUND
            )

        # Подсказки
        help_text = "[↑/↓] SELECT   [ENTER] USE   [D] DROP   [ESC] CLOSE"
        self.console.print(
            x=x + (inventory_width - len(help_text)) // 2,
            y=y + inventory_height - 2,
            string=help_text,
            fg=UI_REGULAR_TEXT,
            bg=UI_BACKGROUND
        )

    def render(self) -> None:
        """Отрисовывает игровое состояние."""
        self.console.clear()

        # Обновляем FOV
        self.game_map.update_fov(self.player.x, self.player.y, radius=8)

        # Отрисовываем карту
        for y in range(self.game_map.height):
            for x in range(self.game_map.width):
                if self.game_map.visible[y, x]:
                    # Если клетка видима, рисуем ее актуальным цветом
                    if self.game_map.tiles[y, x]:
                        self.console.print(x=x, y=y, string=".", fg=FLOOR_COLOR)
                    else:
                        self.console.print(x=x, y=y, string="#", fg=WALL_COLOR)
                elif self.game_map.explored[y, x]:
                    # Если клетка исследована, но не видима, рисуем ее приглушенным цветом
                    if self.game_map.tiles[y, x]:
                        self.console.print(x=x, y=y, string=".", fg=FLOOR_COLOR_DARK)
                    else:
                        self.console.print(x=x, y=y, string="#", fg=WALL_COLOR_DARK)

        # Отрисовываем предметы
        for item in self.game_map.items:
            if self.game_map.visible[item.y, item.x]:
                item.draw(self.console)

        # Отрисовываем сущности
        for entity in self.game_map.entities:
            if self.game_map.visible[entity.y, entity.x]:
                entity.draw(self.console)

        # Создаем фон для HUD
        for y in range(self.map_height, self.screen_height):
            for x in range(self.screen_width):
                self.console.print(x=x, y=y, string=" ", bg=UI_BACKGROUND)

        # Отрисовываем рамку для HUD
        for x in range(self.screen_width):
            self.console.print(
                x=x,
                y=self.map_height,
                string="═",
                fg=UI_KEYS,
                bg=UI_BACKGROUND,
            )

        # Отрисовываем статистику игрока
        hp_color = (
            HEALTH_GOOD if self.player.stats.current_hp > self.player.stats.max_hp * 0.7
            else HEALTH_WARNING if self.player.stats.current_hp > self.player.stats.max_hp * 0.3
            else HEALTH_CRITICAL
        )
        
        # Статистика с подписями
        self.console.print(
            x=2,
            y=self.map_height + 1,
            string="HEALTH:",
            fg=UI_TEXT,
            bg=UI_BACKGROUND,
        )
        self.console.print(
            x=12,
            y=self.map_height + 1,
            string=f"{self.player.stats.current_hp}/{self.player.stats.max_hp}",
            fg=hp_color,
            bg=UI_BACKGROUND,
        )

        self.console.print(
            x=25,
            y=self.map_height + 1,
            string="DAMAGE:",
            fg=UI_TEXT,
            bg=UI_BACKGROUND,
        )
        self.console.print(
            x=32,
            y=self.map_height + 1,
            string=str(self.player.stats.attack_power),
            fg=UI_KEYS,
            bg=UI_BACKGROUND,
        )

        self.console.print(
            x=40,
            y=self.map_height + 1,
            string="DEFENSE:",
            fg=UI_TEXT,
            bg=UI_BACKGROUND,
        )
        self.console.print(
            x=48,
            y=self.map_height + 1,
            string=str(self.player.stats.defense),
            fg=UI_KEYS,
            bg=UI_BACKGROUND,
        )

        # Отрисовываем подсказки по управлению с цветными клавишами
        help_text = [
            ("CONTROL: ", UI_TEXT),
            ("[↑↓←→]", UI_KEYS),
            (" MOVEMENT   ", UI_REGULAR_TEXT),
            ("[I]", UI_KEYS),
            (" INVENTORY   ", UI_REGULAR_TEXT),
            ("[G]", UI_KEYS),
            (" PICK UP   ", UI_REGULAR_TEXT),
            ("[ESC]", UI_KEYS),
            (" EXIT", UI_REGULAR_TEXT),
        ]

        x_pos = 2
        for text, color in help_text:
            self.console.print(
                x=x_pos,
                y=self.map_height + 3,
                string=text,
                fg=color,
                bg=UI_BACKGROUND,
            )
            x_pos += len(text)

        # Отрисовываем легенду с цветными символами
        legend_parts = [
            ("ENTITIES: ", UI_TEXT),
            ("[@]", PLAYER_COLOR),
            (" PLAYER   ", UI_REGULAR_TEXT),
            ("[r]", RAT_COLOR),
            (" RAT   ", UI_REGULAR_TEXT),
            ("[O]", ORC_COLOR),
            (" ORC   ", UI_REGULAR_TEXT),
            ("[T]", TROLL_COLOR),
            (" TROLL", UI_REGULAR_TEXT),
        ]

        x_pos = 2
        for text, color in legend_parts:
            self.console.print(
                x=x_pos,
                y=self.map_height + 5,
                string=text,
                fg=color,
                bg=UI_BACKGROUND,
            )
            x_pos += len(text)

        # Отрисовываем инвентарь поверх всего, если он открыт
        if self.show_inventory:
            self.render_inventory()

        self.context.present(self.console)

    def handle_inventory_input(self, event: tcod.event.Event) -> bool:
        """Обрабатывает ввод в режиме инвентаря."""
        if isinstance(event, tcod.event.KeyDown):
            if event.sym == tcod.event.K_ESCAPE:
                self.show_inventory = False
            elif event.sym == tcod.event.K_UP:
                self.selected_item_index = max(0, self.selected_item_index - 1)
            elif event.sym == tcod.event.K_DOWN:
                self.selected_item_index = min(len(self.player.inventory.items) - 1, self.selected_item_index + 1)
            elif event.sym == tcod.event.K_RETURN:
                if 0 <= self.selected_item_index < len(self.player.inventory.items):
                    item = self.player.inventory.items[self.selected_item_index]
                    self.player.use_item(item)
                    self.show_inventory = False
            elif event.sym == tcod.event.K_d:
                if 0 <= self.selected_item_index < len(self.player.inventory.items):
                    item = self.player.inventory.items[self.selected_item_index]
                    self.player.drop_item(item)
                    self.show_inventory = False
        return False

    def handle_input(self, event: tcod.event.Event) -> bool:
        """Обрабатывает пользовательский ввод."""
        if isinstance(event, tcod.event.Quit):
            return True

        if self.show_inventory:
            return self.handle_inventory_input(event)

        if isinstance(event, tcod.event.KeyDown):
            if event.sym == tcod.event.K_ESCAPE:
                return True

            # Движение
            if event.sym == tcod.event.K_UP:
                self._try_move_player(0, -1)
            elif event.sym == tcod.event.K_DOWN:
                self._try_move_player(0, 1)
            elif event.sym == tcod.event.K_LEFT:
                self._try_move_player(-1, 0)
            elif event.sym == tcod.event.K_RIGHT:
                self._try_move_player(1, 0)
            elif event.sym == tcod.event.K_i:
                self.show_inventory = True
                self.selected_item_index = 0
            elif event.sym == tcod.event.K_g:
                # Подбираем предметы с земли
                items = self.game_map.get_items_at(self.player.x, self.player.y)
                for item in items:
                    if self.player.pick_up_item(item):
                        break  # Подбираем только один предмет за раз

        return False

    def _try_move_player(self, dx: int, dy: int) -> None:
        """Пытается переместить игрока."""
        dest_x = self.player.x + dx
        dest_y = self.player.y + dy

        if not self.game_map.in_bounds(dest_x, dest_y):
            return

        target = self.game_map.get_blocking_entity_at(dest_x, dest_y)
        if target:
            self.player.attack(target)
            if not target.is_alive():
                self.game_map.remove_entity(target)
        elif self.game_map.is_walkable(dest_x, dest_y):
            self.player.move(dx, dy)

    def game_loop(self) -> None:
        """Основной игровой цикл."""
        self.initialize()

        while True:
            self.render()

            for event in tcod.event.wait():
                if self.handle_input(event):
                    return  # Выход из игры

            # Проверяем состояние игрока
            if not self.player.is_alive():
                return  # Игра окончена 