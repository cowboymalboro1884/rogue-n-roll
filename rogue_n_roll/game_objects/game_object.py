from typing import Optional
import tcod.console


class GameObject:
    def __init__(
        self,
        x: int,
        y: int,
        char: str,
        color: tuple[int, int, int],
        name: str,
        is_blocking: bool = False,
        is_walkable: bool = True,
    ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.is_blocking = is_blocking
        self.is_walkable = is_walkable

    def draw(self, console: tcod.console.Console) -> None:
        """Отрисовывает объект на консоли."""
        console.print(x=self.x, y=self.y, string=self.char, fg=self.color)

    def move(self, dx: int, dy: int) -> None:
        """Перемещает объект на dx, dy клеток."""
        self.x += dx
        self.y += dy 