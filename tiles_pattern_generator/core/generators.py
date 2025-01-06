import random
from typing import List, Literal, Tuple

from tiles_pattern_generator.core.commons.enums import TileType, Direction
from tiles_pattern_generator.core.tile import Tile


class ColorGenerator:
    def __init__(self, colors:List[int]):
        valid_colors = [i for i in colors if 0 <= i <= 0xffffff]
        if len(valid_colors) == 0:
            valid_colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(10)]
        self.colors =valid_colors

    @property
    def random_color(self) -> list:
        return random.choice(self.colors)
    
class DesignGenerator:
    def __init__(self, arcs_probability:float, directions:str):
        if arcs_probability < 0 or arcs_probability > 1:
            raise ValueError(f"Invalid arcs_probability value {arcs_probability}")
        if directions not in ['mixed', 'horizontal', 'vertical']:
            raise ValueError(f"Invalid direction value {directions}")   
        self.arcs_probability = arcs_probability
        self.directions = directions

    def random_tile(self) -> Tuple[TileType, Literal[0, 1, 2, 3]]:
        tile_type = TileType.ARKS if random.random() < self.arcs_probability else TileType.LINES
        match self.directions:
            case 'mixed':
                direction = random.choice([0, 1, 2, 3])
            case 'horizontal':
                direction = 1
            case 'vertical':
                direction = 0
        return tile_type, direction