# levels/level_manager.py
from levels.grid_parser import LevelParser

# Reconstrucción del Nivel 1 A* basado en las restricciones de 10x10
LEVEL_1_STR = """
....#..G.E
.....#....
..#.......
#.......#.
.#...#..#.
....#.....
...#..##..
.#...##...
.##..#..#.
P....#....
"""

class LevelManager:
    def __init__(self):
        self.current_level = 1
        self.parser = LevelParser(LEVEL_1_STR)

    def get_current_grid(self):
        return self.parser.grid