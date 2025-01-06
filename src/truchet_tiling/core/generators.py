import random
from typing import List, Literal, Tuple

from truchet_tiling.commons.enums import TileType


class ColorGenerator:
    def __init__(self, colors:List[int]):
        valid_colors = [i for i in colors if 0 <= i <= 0xffffff]
        if len(valid_colors) == 0:
            valid_colors = [random.randint(0, 0xffffff) for _ in range(10)]
        self.colors = valid_colors

    @property
    def random_color(self) -> int:
        return random.choice(self.colors)
    
class DesignGenerator:
    def __init__(self, arcs_probability:float, directions:str):
        if arcs_probability < 0 or arcs_probability > 1:
            raise ValueError(f"Invalid arcs_probability value {arcs_probability}")
        if directions not in ['mixed', 'horizontal', 'vertical']:
            raise ValueError(f"Invalid direction value {directions}")   
        self.arcs_probability = arcs_probability
        self.directions = directions

    def get_design(self) -> Tuple[TileType, Literal[0, 1, 2, 3]]:
        tile_type = TileType.ARKS if random.random() < self.arcs_probability else TileType.LINES
        match self.directions:
            case 'mixed':
                direction = random.choice([0, 1, 2, 3])
            case 'horizontal':
                direction = 2
            case 'vertical':
                direction = 3
        return tile_type, direction