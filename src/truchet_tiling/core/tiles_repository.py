import importlib.resources
import truchet_tiling.static.truchet_tiles_01 as tt
import truchet_tiling.static.triangles as triangles
from truchet_tiling.commons.enums import TileType
import svgwrite
from xml.etree import ElementTree as ET

class TilesRepository:
    def __init__(self):
        files = ["arcs1", "arcs2", "arcs4", "lines1", "lines2", "lines4"]
        self._files = {}
        #print current directory
        for file in files:
            with importlib.resources.path(tt, f'{file}.svg') as fspath:
                with open(str(fspath), "r") as f:
                    svg_data = f.read()
                    self._files[file] = svg_data

    def get(self, size:int, pattern:TileType) -> str:
        if size not in [1, 2, 4]:
            raise ValueError("Size must be one of 1, 2, 4")
        match pattern:
            case TileType.ARKS:
                key = f"arcs{size}"
            case TileType.LINES:
                key = f"lines{size}"
            case _:
                raise ValueError("Wrong tile type")
        svg_data = self._files[key]
        return svg_data
    
    def get_triangle(self) -> ET.Element:
        with importlib.resources.path(triangles, 'triangle.svg') as fspath:
            tree = ET.parse(fspath)
            root = tree.getroot()
            return root

