from io import BytesIO
from core.commons.constants import TILE_SIZE
from core.demo_tile import DemoTile
from core.pattern import Pattern
from core.tile import Tile
import cairo
import cairosvg

patterns = Pattern()

def draw(ctx, tile:Tile):
    x = tile.x
    y = tile.y
    s = tile.size
    screen_size = s * TILE_SIZE
    svg_data = patterns.get(s, tile.type)
    for i, stroke in enumerate(tile.strokes):
        color_name = f'{{fill{i}}}'
        new_color = stroke.color if stroke.color else "#ffffff"
        svg_data = svg_data.replace(color_name, new_color)
        svg_data = svg_data.replace(r"{stroke}", "#000")
        svg_data = svg_data.replace(r"{stroke-width}", "8")
    bytes = cairosvg.svg2png(bytestring=svg_data,
                             output_height=screen_size,
                             output_width=screen_size,)  
    surface = cairo.ImageSurface.create_from_png(BytesIO(bytes))
    ctx.save()
    ctx.translate(x * TILE_SIZE + (s * TILE_SIZE) / 2, y * TILE_SIZE + (s * TILE_SIZE) / 2)
    ctx.rotate(tile.rotation)
    ctx.translate(-(s * TILE_SIZE) / 2, -(s * TILE_SIZE) / 2)
    ctx.set_source_surface(surface, 0, 0)
    ctx.paint()
    ctx.restore()

def demo_draw(ctx, tile:DemoTile):
    x = tile.x
    y = tile.y
    s = tile.size
    colors = tile.matrix
    # draw white quadrat with black border in cairo context ctx
    # iterate through 2d numpy array and draw rectangles

    # 1. draw outlines of rectangles
    ctx.set_source_rgb(1, 1, 1)  # set the color to black
    ctx.rectangle(x * TILE_SIZE, y * TILE_SIZE, s * TILE_SIZE, s * TILE_SIZE)
    ctx.stroke()  # draw the outline of the rectangle

    # 2. draw the rectangles
    matrix = tile.matrix._data
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            value = colors._data[i][j]
            color = (2*value + 1)/2
            ctx.set_source_rgb(color, color, color)
            ctx.rectangle((x + i) * TILE_SIZE, (y + j) * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            ctx.fill()