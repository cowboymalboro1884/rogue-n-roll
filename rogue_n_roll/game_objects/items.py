from typing import Tuple, TYPE_CHECKING
from rogue_n_roll.game_objects.item import Item
from rogue_n_roll.engine.colors import POTION_COLOR, SWORD_COLOR, SHIELD_COLOR, SCROLL_COLOR

if TYPE_CHECKING:
    from rogue_n_roll.game_objects.entity import Entity


class HealthPotion(Item):
    def __init__(self, x: int, y: int):
        super().__init__(
            x=x,
            y=y,
            char="!",
            color=POTION_COLOR,
            name="Health Potion",
            description="Restores 4 health points",
        )

    def use(self, user: "Entity") -> bool:
        """Использует зелье здоровья."""
        if user.stats.current_hp < user.stats.max_hp:
            user.stats.heal(4)
            return True
        return False


class Sword(Item):
    def __init__(self, x: int, y: int):
        super().__init__(
            x=x,
            y=y,
            char="/",
            color=SWORD_COLOR,
            name="Sword",
            description="Increases attack power by 2",
        )

    def use(self, user: "Entity") -> bool:
        """Экипирует меч."""
        user.stats.attack_power += 2
        return True


class Shield(Item):
    def __init__(self, x: int, y: int):
        super().__init__(
            x=x,
            y=y,
            char="]",
            color=SHIELD_COLOR,
            name="Shield",
            description="Increases defense by 1",
        )

    def use(self, user: "Entity") -> bool:
        """Экипирует щит."""
        user.stats.defense += 1
        return True


class ScrollOfLightning(Item):
    def __init__(self, x: int, y: int):
        super().__init__(
            x=x,
            y=y,
            char="?",
            color=SCROLL_COLOR,
            name="Lightning Scroll",
            description="Deals 6 damage to nearest enemy",
        )

    def use(self, user: "Entity") -> bool:
        """Использует свиток молнии."""
        if not user.game_map:
            return False

        # Находим ближайшего врага
        closest_enemy = None
        closest_distance = float("inf")

        for entity in user.game_map.entities:
            if entity != user and entity.is_alive():
                distance = ((entity.x - user.x) ** 2 + (entity.y - user.y) ** 2) ** 0.5
                if distance < closest_distance:
                    closest_enemy = entity
                    closest_distance = distance

        if closest_enemy and closest_distance <= 5:  # Максимальная дальность 5 клеток
            closest_enemy.stats.take_damage(6)
            return True

        return False 