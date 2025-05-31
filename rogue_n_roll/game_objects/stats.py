from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class Stats:
    max_hp: int
    current_hp: int
    attack_power: int
    defense: int
    speed: int = 1
    modifiers: Dict[str, int] = None

    def __post_init__(self):
        if self.modifiers is None:
            self.modifiers = {}

    def get_effective_stat(self, stat_name: str) -> int:
        """Возвращает значение характеристики с учетом модификаторов."""
        base_value = getattr(self, stat_name, 0)
        modifier = self.modifiers.get(stat_name, 0)
        return base_value + modifier

    def take_damage(self, amount: int) -> None:
        """Наносит урон, уменьшая текущее здоровье."""
        self.current_hp = max(0, self.current_hp - amount)

    def heal(self, amount: int) -> None:
        """Восстанавливает здоровье."""
        self.current_hp = min(self.max_hp, self.current_hp + amount)

    def is_alive(self) -> bool:
        """Проверяет, жива ли сущность."""
        return self.current_hp > 0

    def add_modifier(self, stat_name: str, value: int) -> None:
        """Добавляет модификатор к характеристике."""
        self.modifiers[stat_name] = self.modifiers.get(stat_name, 0) + value

    def remove_modifier(self, stat_name: str, value: int) -> None:
        """Удаляет модификатор характеристики."""
        if stat_name in self.modifiers:
            self.modifiers[stat_name] = max(0, self.modifiers[stat_name] - value)
            if self.modifiers[stat_name] == 0:
                del self.modifiers[stat_name] 