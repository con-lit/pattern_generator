import argparse
import random
import math
import svgwrite
from io import StringIO
from svgpathtools import svg2paths

from truchet_tiling.core.drawing import Drawing
from truchet_tiling.core.svg_utils import get_triangles_translation, translate_path
from truchet_tiling.core.tiles_repository import TilesRepository
from truchet_tiling.core.trees.tritree import TriTree

tiles = TilesRepository()

def demo_draw(drawing:Drawing, vertices:list, position:tuple):
    pass

def draw_triangle( drawing:Drawing, position:tuple, reflected:bool, depth:int):
    rotation = random.choice([0, 120, 240])
    svg = tiles.get_triangle(depth, rotation, scale_y = -1 if reflected else 1)
    paths, attributes = svg2paths(StringIO(svg))
    for path in paths:
        translated_path = translate_path(path, tx=position[0], ty=position[1])
        path_string = translated_path.d()
        path_element = svgwrite.path.Path(
            d=path_string,
            stroke="black",
            fill="none",
            stroke_width=1
        )
        drawing.add(path_element)

def create_tritrees(rows:int, cols:int, cell_width:int, cell_height:int):
    trees = []
    y=0
    for j in range(cols):
        x = 0
        for i in range(rows):
            reflected = bool((i + j % 2) % 2)
            if reflected:
                vertices = [(x+cell_width/2, y), (x, y+cell_height), (x+cell_width, y+cell_height)] 
            else:
                vertices = [(x, y), (x+cell_width, y), (x+cell_width/2, y+cell_height)]
            trees.append(
                TriTree(
                    vertices,
                    depth=2, 
                    reflected=reflected,
                )
            )
            x += cell_width/2
        y += cell_height
    return trees
            

def draw_svg_grid(drw, rows:int, cols:int, cell_width:int, cell_height:int):
    y = 0
    for j in range(cols):
        x = 0
        for i in range(rows):
            scale_y = -1 if bool((i + j % 2) % 2) else 1
            rotation = random.choice([0, 120, 240])
            svg = tiles.get_triangle(rotation, scale_y = scale_y)
            paths, attributes = svg2paths(StringIO(svg))
            for path in paths:
                translated_path = translate_path(path, tx=x, ty=y)
                path_string = translated_path.d()
                path_element = svgwrite.path.Path(
                    d=path_string,
                    stroke="black",
                    fill="none",
                    stroke_width=1
                )
                drw.add(path_element)
            x += math.floor(cell_width/2)
        y += math.floor(cell_height)

def main():
    parser = argparse.ArgumentParser(description="Generate a PNG bitmap and save it to a file.")
    parser.add_argument('--width', type=int, default=6, help="Width of the bitmap")
    parser.add_argument('--height', type=int, default=4, help="Height of the bitmap")
    parser.add_argument('--cell', type=int, default=50, help="Size of a cell")
    parser.add_argument('--color', type=str, default='#00ff00', help="Color of the bitmap (e.g., 'red', '#00ff00')")
    parser.add_argument('--output_file', type=str, default='output.svg', help="Output file path")

    args = parser.parse_args()
    columns = args.width
    rows = args.height
    cell_size = args.cell
    cell_width=200
    cell_hight=3*cell_width/(4*math.cos(math.pi/6))
    image_width = math.ceil((columns / 2 + 1) * cell_width)
    image_height = math.ceil(rows * cell_hight)
    drawing = Drawing(image_width, image_height)

    trees = create_tritrees(rows, columns, cell_width, cell_hight)

    for tree in trees:
        tree.draw_tile(draw_triangle, drawing)

    drawing.save(args.output_file)
    
if __name__ == "__main__":
    main()