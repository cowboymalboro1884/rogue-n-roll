from typing import Optional, Tuple
from rogue_n_roll.game_objects.entity import Entity
from rogue_n_roll.game_objects.stats import Stats


class Player(Entity):
    def __init__(
        self,
        x: int,
        y: int,
        char: str = "@",
        color: Tuple[int, int, int] = (255, 255, 0),
        name: str = "Игрок",
    ):
        stats = Stats(
            max_hp=30,
            current_hp=30,
            attack_power=5,
            defense=2,
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