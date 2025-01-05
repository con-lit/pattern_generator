from tiles_pattern_generator.core.commons.enums import Design, Direction, Theme
from tiles_pattern_generator.core.pattern_creator import truchet_tiles

def generate_bitmap(width:int = 100, height = 100, design = Design.MIXED, directions = Direction.MIXED, theme = Theme.RANDOM):
    image = truchet_tiles(width, height, design, directions, theme)
    return image 