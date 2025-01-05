from tiles_pattern_generator.core.commons.enums import TileType
import os

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
        print(os.getcwd())
        for file in files:
            with open(f"./static/svg/{file}.svg", "r") as f:
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
    
    def get_filename(self, size:int, pattern:str):
        if size not in [1, 2, 4]:
            raise ValueError("Size must be one of 1, 2, 4")
        if pattern not in ["round", "straight"]:    
            raise ValueError("Pattern must be one of 'round', 'straight'")
        return f"./tiles_pattern_generator/static/svg/{pattern}_{size}.svg"

