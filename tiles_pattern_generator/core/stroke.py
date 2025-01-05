from typing import Dict, List
from core.commons.enums import Side

class Stroke:
    _connectors:Dict[Side, List]
    _color:tuple

    def __init__(self):
        self._color = None
        self._connectors = {}

    @property
    def color(self):
        return self._color

    def add_link(self, side:Side, link, stroke_id:int):
        from core.commons.data_classes import Connection
        if link is None:
            self._connectors[side] = []
        else:
            connection = Connection(link, stroke_id)
            if side not in self._connectors:
                self._connectors[side] = [connection]
            else:
                self._connectors[side].append(connection)

    def set_color(self, new_color):
        if self._color == new_color:
            return
        self._color = new_color
        sides = self._connectors.keys()
        for output_side in sides:
            connectors = self._connectors[output_side]
            if connectors is not None:
                for connector in connectors:
                    link = connector.link
                    link.tile.color_stroke(new_color,
                                           output_side.opposite,
                                           link.interface_id,
                                           connector.stroke_id)