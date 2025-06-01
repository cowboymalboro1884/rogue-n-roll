from typing import Optional, Tuple
from rogue_n_roll.game_objects.entity import Entity
from rogue_n_roll.game_objects.stats import Stats


class Monster(Entity):
    def __init__(
        self,
        x: int,
        y: int,
        char: str,
        color: Tuple[int, int, int],
        name: str,
        max_hp: int,
        attack_power: int,
        defense: int,
    ):
        stats = Stats(
            max_hp=max_hp,
            current_hp=max_hp,
            attack_power=attack_power,
            defense=defense,
        )
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            stats=stats,
            is_blocking=True,
        )

    def attack(self, target: Entity) -> None:
        """Атакует цель."""
        damage = max(0, self.stats.get_effective_stat("attack_power") - target.stats.get_effective_stat("defense"))
        if damage > 0:
            target.take_damage(damage)
        else:
            # Минимальный урон всегда 1
            target.take_damage(1)

    @staticmethod
    def create_rat(x: int, y: int) -> "Monster":
        return Monster(
            x=x,
            y=y,
            char="r",
            color=(150, 150, 150),  # Серый цвет для крыс
            name="Крыса",
            max_hp=5,
            attack_power=2,
            defense=0,
        )

    @staticmethod
    def create_orc(x: int, y: int) -> "Monster":
        return Monster(
            x=x,
            y=y,
            char="O",  # Заглавная O для лучшей видимости
            color=(0, 255, 0),  # Ярко-зеленый для орков
            name="Орк",
            max_hp=10,
            attack_power=4,
            defense=1,
        )

    @staticmethod
    def create_troll(x: int, y: int) -> "Monster":
        return Monster(
            x=x,
            y=y,
            char="T",
            color=(255, 0, 0),  # Красный для троллей
            name="Тролль",
            max_hp=20,
            attack_power=6,
            defense=2,
        ) 