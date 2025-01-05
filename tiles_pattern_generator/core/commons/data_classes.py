from dataclasses import dataclass


@dataclass
class Link:
    from tiles_pattern_generator.core.commons.enums import Side
    from tiles_pattern_generator.core.tile import Tile
    tile: Tile
    side: Side
    interface_id: int

@dataclass
class Connection:
    link: Link
    stroke_id: int
