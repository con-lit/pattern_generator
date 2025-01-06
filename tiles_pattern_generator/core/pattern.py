from tiles_pattern_generator.core.commons.enums import TileType
import os
import pkg_resources

class Pattern:
    def __init__(self):
        files = [
            "arcs1",
            "arcs2",
            "arcs4",
            "lines1",
            "lines2",
            "lines4",
        ]
        self._files = {}
        #print current directory
        for file in files:
            svg_path = pkg_resources.resource_filename(__name__, f'static/truchet_tiles_01/{file}.svg')
            with open(svg_path, "r") as f:
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

