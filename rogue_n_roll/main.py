#!/usr/bin/env python3
import traceback
import tcod
from rogue_n_roll.engine.game_engine import GameEngine


def main() -> None:
    try:
        engine = GameEngine()
        engine.game_loop()
    except Exception as e:
        traceback.print_exc()
        input("\nНажмите Enter для выхода...")


if __name__ == "__main__":
    main() 