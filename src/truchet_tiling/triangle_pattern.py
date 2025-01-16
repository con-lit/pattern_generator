import argparse
import random
import math
import svgwrite
from io import StringIO
from svgpathtools import svg2paths

from truchet_tiling.commons.constants import TRI_CELL_HEIGHT, TRI_CELL_WIDTH
from truchet_tiling.core.connector_new import ConnectorNew
from truchet_tiling.core.drawing import Drawing
from truchet_tiling.core.svg_utils import get_triangles_translation, translate_path
from truchet_tiling.core.tiles_repository import TilesRepository
from truchet_tiling.core.trees.tritree import TriTree
from truchet_tiling.core.fills.gradient import Gradient
from truchet_tiling.core.fills.perlin import Perlin

tiles = TilesRepository()

def draw( drawing:Drawing, position:tuple, reflected:bool, depth:int, uuid:str, connector:ConnectorNew):
    rotation = random.choice([0, 120, 240])
    svg = tiles.get_triangle(depth, rotation, scale_y = -1 if reflected else 1)
    paths, attributes = svg2paths(StringIO(svg))
    for i, path in enumerate(paths):
        path_id = f'{uuid}-{attributes[i]["id"]}'
        translated_path = translate_path(path, tx=position[0], ty=position[1])
        begin = translated_path.start
        end = translated_path.end
        connector.register_path(
            (begin.real, begin.imag),
            (end.real, end.imag),
            path_id
        )
        print(f"Path {path_id} starts at {begin} and ends at {end}")
        path_string = translated_path.d()
        path_element = svgwrite.path.Path(
            d=path_string,
            stroke="black",
            fill="none",
            stroke_width=1,
            id=path_id
        )
        drawing.add(path_element)

def create_tritrees(columns:int, rows:int, matrix:Perlin, connector:ConnectorNew):
    trees = []
    y=0
    for j in range(rows):
        x = 0
        for i in range(columns):
            reflected = bool((i + j % 2) % 2)
            if reflected:
                vertices = [(x+TRI_CELL_WIDTH/2, y), (x, y+TRI_CELL_HEIGHT), (x+TRI_CELL_WIDTH, y+TRI_CELL_HEIGHT)] 
            else:
                vertices = [(x, y), (x+TRI_CELL_WIDTH, y), (x+TRI_CELL_WIDTH/2, y+TRI_CELL_HEIGHT)]
            trees.append(TriTree(
                vertices, 
                depth=2,
                reflected=reflected,    
                matrix=matrix,
                connector=connector,
            ))
            x += TRI_CELL_WIDTH/2
        y += TRI_CELL_HEIGHT
    return trees
            
def main():
    parser = argparse.ArgumentParser(description="Generate a PNG bitmap and save it to a file.")
    parser.add_argument('--width', type=int, default=6, help="Width of the bitmap")
    parser.add_argument('--height', type=int, default=4, help="Height of the bitmap")
    parser.add_argument('--cell', type=int, default=50, help="Size of a cell")
    parser.add_argument('--color', type=str, default='#00ff00', help="Color of the bitmap (e.g., 'red', '#00ff00')")
    parser.add_argument('--output', type=str, default='output.svg', help="Output file path")

    args = parser.parse_args()
    columns = args.width
    rows = args.height
    cell_size = args.cell
    
    drawing_width = TRI_CELL_WIDTH * (math.ceil(columns / 2) + (1 - columns % 2) / 2)
    drawing_height = rows * TRI_CELL_HEIGHT
    print("Image size: ", drawing_width, drawing_height)
    
    matrix = Perlin(math.ceil(drawing_width), math.ceil(drawing_height), octaves=4)
    connector = ConnectorNew()
    # matrix = Gradient('linear', math.ceil(drawing_width), math.ceil(drawing_height))

    drawing = Drawing(drawing_width, drawing_height)

    trees = create_tritrees(columns, rows, matrix, connector)

    for tree in trees:
        tree.draw_tile(draw, drawing)

    drawing.save(args.output)
    clusters = connector.cluster_points()
    print(clusters)
    
if __name__ == "__main__":
    main()