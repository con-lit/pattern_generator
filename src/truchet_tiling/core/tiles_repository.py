import importlib.resources
from truchet_tiling.core.svg_utils import get_trialgles_translation, translate_path
import truchet_tiling.static.truchet_tiles_01 as tt
import truchet_tiling.static.triangles as triangles
from truchet_tiling.commons.enums import TileType
import svgwrite
from xml.etree import ElementTree as ET
from svgpathtools import svg2paths

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
    
    def get_triangle(self, r, scale_x=1, scale_y=1) -> str:
        with importlib.resources.path(triangles, 'triangle.svg') as fspath:
            tree = ET.parse(fspath)
            root = tree.getroot()

            width = root.get('width', '100%')
            height = root.get('height', '100%')
            view_box = root.get('viewBox', '0 0 100 100')
            vb_x, vb_y, vb_width, vb_height = map(float, view_box.split())

            dwg = svgwrite.Drawing(size=(width, height))
            dwg.viewbox(*[vb_x, vb_y, vb_width, vb_height])

            paths, attributes = svg2paths(fspath)

            for path in paths:
                tx, ty = get_trialgles_translation(r, vb_width, vb_height, scale_x, scale_y)
                translated_path = translate_path(path, r=r, tx=tx, ty=ty, sx=scale_x, sy=scale_y)
                path_string = translated_path.d()
                path_element = svgwrite.path.Path(
                    d=path_string,
                    stroke="black",
                    fill="none",
                    stroke_width=1
                )
                dwg.add(path_element)
            
            return dwg.tostring()

