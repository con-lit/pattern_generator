import argparse
from io import BytesIO
from cairo import FORMAT_ARGB32, Context, ImageSurface
import math
from xml.etree import ElementTree as ET

import cairo
import cairosvg

from truchet_tiling.core.tiles_repository import TilesRepository

tiles = TilesRepository()

def draw_grid(ctx: Context, rows, cols, cell_width, cell_height):
    for j in range(cols):
        for i in range(rows):
            x = i * cell_width/2
            y = j * cell_height
            reflection = bool((i + j % 2) % 2)
            svg = tiles.get_triangle()
            scale = int(svg.get("viewBox").split(" ")[2])/cell_width
            if reflection:
                svg.set("transform", f"scale(1, -1) translate(0, {-scale * cell_height})")
            svg_data = ET.tostring(svg, encoding='utf-8', method='xml')
            bytes = cairosvg.svg2png(
                bytestring=svg_data,
                output_height=cell_height,
                output_width=cell_width,
            )  
            surface = ImageSurface.create_from_png(BytesIO(bytes))
            ctx.save()
            ctx.translate(x , y)
            ctx.set_source_surface(surface, 0, 0)
            ctx.paint()
            ctx.restore()
    

def main():
    parser = argparse.ArgumentParser(description="Generate a PNG bitmap and save it to a file.")
    parser.add_argument('--width', type=int, default=6, help="Width of the bitmap")
    parser.add_argument('--height', type=int, default=4, help="Height of the bitmap")
    parser.add_argument('--cell', type=int, default=50, help="Size of a cell")
    parser.add_argument('--color', type=str, default='#00ff00', help="Color of the bitmap (e.g., 'red', '#00ff00')")
    parser.add_argument('--output_file', type=str, default='output.png', help="Output file path")

    args = parser.parse_args()
    columns = args.width
    rows = args.height
    cell_size = args.cell
    cell_width=cell_size
    cell_hight=cell_hight=3*cell_size/(4*math.cos(math.pi/6))
    image_width = math.ceil((columns / 2 + 1) * cell_width)
    image_height = math.ceil(rows * cell_hight)
    surface = ImageSurface(FORMAT_ARGB32, image_width, image_height)
    draw_grid(Context(surface), columns, rows, cell_width, cell_hight)

    with cairo.ImageSurface(
        cairo.FORMAT_ARGB32,
        image_width - math.floor(3*cell_width/2), 
        image_height
    ) as cropped_surface:
        cropped_ctx = cairo.Context(cropped_surface)
        cropped_ctx.translate(- cell_width/2, 0)
        cropped_ctx.set_source_surface(surface)
        cropped_ctx.paint()
        cropped_surface.write_to_png('output_file.png')

if __name__ == "__main__":
    main()