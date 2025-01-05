from enum import Enum


class Side(Enum):
  TOP = 0
  RIGHT = 1
  BOTTOM = 2
  LEFT = 3

  @property
  def opposite(self):
    if self == Side.TOP:
      return Side.BOTTOM
    elif self == Side.LEFT:
      return Side.RIGHT
    elif self == Side.BOTTOM:
      return Side.TOP
    elif self == Side.RIGHT:
      return Side.LEFT

  @property
  def corner(self):
    if self == Side.TOP:
      return Side.LEFT
    elif self == Side.LEFT:
      return Side.TOP
    elif self == Side.BOTTOM:
      return Side.RIGHT
    elif self == Side.RIGHT:
      return Side.BOTTOM

class TileType(Enum):
    ARKS = 0
    LINES = 1

class Design(Enum):
    MIXED = "mixed_designs"
    MORE_LINES = "more_lines"
    MORE_ARCS = "more_arcs"
    ONLY_LINES = "only_lines"
    ONLY_ARCS = "only_arcs"

class Direction(Enum):
    MIXED = "mixed_directions"
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"

class Theme(Enum):
    GREEN = "green"
    MORDOR = "mordor"
    RANDOM = "random"