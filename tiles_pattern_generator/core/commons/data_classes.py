from dataclasses import dataclass


@dataclass
class Link:
    from core.commons.enums import Side
    from core.tile import Tile
    tile: Tile
    side: Side
    interface_id: int

@dataclass
class Connection:
    link: Link
    stroke_id: int
