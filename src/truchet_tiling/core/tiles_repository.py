import importlib.resources
from truchet_tiling.core.svg_utils import get_triangles_translation, translate_path
import truchet_tiling.static.truchet_tiles_01 as tt
import truchet_tiling.static.triangles as triangles
from truchet_tiling.commons.enums import TileType
import svgwrite
from xml.etree import ElementTree as ET
from svgpathtools import svg2paths

class TilesRepository:
    def __init__(self):
        files = ["arcs1", "arcs2", "arcs4", "lines1", "lines2", "lines4"]
        self.triangles = {
            0: "triangle_1.svg",
            1: "triangle_2.svg",
            2: "triangle_4.svg",
        }
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
    
    def get_triangle(self, version, rotation, scale_x=1, scale_y=1) -> str:
        if version not in self.triangles:
            raise ValueError(f"Invalid triangle version {version}")
        with importlib.resources.path(triangles, self.triangles[version]) as fspath:
            tree = ET.parse(fspath)
            root = tree.getroot()

            width = root.get('width', '100%')
            height = root.get('height', '100%')
            view_box = root.get('viewBox', '0 0 100 100')
            vb_x, vb_y, vb_width, vb_height = map(float, view_box.split())

            dwg = svgwrite.Drawing(size=(width, height))
            dwg.viewbox(*[vb_x, vb_y, vb_width, vb_height])

            paths, attributes = svg2paths(fspath)

            for i, path in enumerate(paths):
                id = attributes[i]["id"]
                tx, ty = get_triangles_translation(rotation, vb_width, vb_height, scale_x, scale_y)
                translated_path = translate_path(path, r=rotation, tx=tx, ty=ty, sx=scale_x, sy=scale_y)
                path_string = translated_path.d()
                path_element = svgwrite.path.Path(
                    d=path_string,
                    stroke="black",
                    fill="none",
                    stroke_width=1,
                    id=id
                )
                dwg.add(path_element)
            
            return dwg.tostring()

