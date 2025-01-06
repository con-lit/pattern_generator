from dataclasses import dataclass


@dataclass
class Link:
    from truchet_tiling.commons.enums import Side
    from truchet_tiling.core.tile import Tile
    tile: Tile
    side: Side
    interface_id: int

@dataclass
class Connection:
    link: Link
    stroke_id: int
