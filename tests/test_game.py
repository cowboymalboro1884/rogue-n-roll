import pytest
import numpy as np
from rogue_n_roll.game_objects.player import Player
from rogue_n_roll.game_objects.monster import Monster
from rogue_n_roll.game_objects.stats import Stats
from rogue_n_roll.map.game_map import GameMap
from rogue_n_roll.map.map_generator import MapGenerator


class TestFunctional:
    """Функциональные тесты."""

    def test_player_movement(self):
        """FT-01: Тест перемещения игрока."""
        game_map = GameMap(10, 10)
        game_map.tiles[5, 5] = True  # Проходимая клетка
        game_map.tiles[6, 5] = True  # Проходимая клетка для движения вниз
        player = Player(5, 5)
        game_map.add_entity(player)

        # Проверяем, что игрок привязан к карте
        assert player.game_map is game_map

        # Перемещение в проходимую клетку
        assert player.move(0, 1) is True
        assert (player.x, player.y) == (5, 6)

        # Попытка пройти сквозь стену
        game_map.tiles[7, 5] = False  # Непроходимая клетка
        assert player.move(0, 1) is False
        assert (player.x, player.y) == (5, 6)  # Позиция не изменилась

    def test_map_generation(self):
        """FT-02: Тест генерации карты."""
        map_generator = MapGenerator(80, 45)
        
        # Генерируем несколько карт и проверяем, что они разные
        game_map1, rooms1 = map_generator.generate_map()
        game_map2, rooms2 = map_generator.generate_map()

        # Карты должны быть разными
        assert not np.array_equal(game_map1.tiles, game_map2.tiles)
        
        # Проверяем, что на карте есть и стены, и проходимые участки
        assert np.any(game_map1.tiles)  # Есть проходимые клетки
        assert not np.all(game_map1.tiles)  # Есть непроходимые клетки

    def test_character_stats(self):
        """FT-03: Тест характеристик персонажа."""
        player = Player(0, 0)
        
        # Проверяем начальные характеристики
        assert player.stats.max_hp == 30
        assert player.stats.current_hp == 30
        assert player.stats.attack_power == 5
        assert player.stats.defense == 2

        # Проверяем отображение характеристик через эффективные значения
        assert player.stats.get_effective_stat("attack_power") == 5
        assert player.stats.get_effective_stat("defense") == 2

    def test_combat(self):
        """FT-05: Тест боевой системы."""
        game_map = GameMap(10, 10)
        player = Player(1, 1)
        monster = Monster.create_rat(2, 1)  # Крыса: HP=5, атака=2, защита=0
        
        game_map.add_entity(player)
        game_map.add_entity(monster)

        # Игрок атакует монстра
        initial_monster_hp = monster.stats.current_hp
        player.attack(monster)
        # Урон = атака игрока (5) - защита монстра (0) = 5
        assert monster.stats.current_hp == initial_monster_hp - 5
        assert not monster.is_alive()  # Крыса должна умереть от одного удара

        # Тест с более сильным монстром
        troll = Monster.create_troll(2, 1)  # Тролль: HP=20, атака=6, защита=2
        game_map.add_entity(troll)
        
        initial_troll_hp = troll.stats.current_hp
        player.attack(troll)
        # Урон = атака игрока (5) - защита тролля (2) = 3
        assert troll.stats.current_hp == initial_troll_hp - 3
        assert troll.is_alive()  # Тролль должен выжить после одного удара

    def test_permanent_death(self):
        """FT-06: Тест системы перманентной смерти."""
        player = Player(0, 0)
        assert player.is_alive()

        # Наносим урон, но не смертельный
        player.take_damage(20)
        assert player.stats.current_hp == 10
        assert player.is_alive()

        # Наносим смертельный урон
        player.take_damage(15)
        assert player.stats.current_hp == 0
        assert not player.is_alive()

    def test_fov(self):
        """FT-07: Тест поля зрения."""
        game_map = GameMap(10, 10)
        # Создаем коридор и делаем все стены непрозрачными
        game_map.tiles.fill(False)  # Сначала все стены
        game_map.tiles[5, :] = True  # Затем коридор
        
        player = Player(5, 0)
        game_map.add_entity(player)
        
        # Обновляем поле зрения
        game_map.update_fov(player.x, player.y, radius=8)
        
        # Проверяем, что клетки в коридоре видны
        assert game_map.visible[0, 5]  # Клетка под игроком должна быть видна
        assert not game_map.visible[0, 0]  # Клетка за стеной не должна быть видна

        # Проверяем, что исследованные клетки запоминаются
        assert game_map.explored[0, 5]
        game_map.visible.fill(False)
        assert game_map.explored[0, 5]  # Клетка должна оставаться исследованной 