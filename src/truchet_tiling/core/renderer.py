from io import BytesIO
from truchet_tiling.core.demo_tile import DemoTile
from truchet_tiling.core.pattern import Pattern
from truchet_tiling.core.tile import Tile
from cairo import Context, ImageSurface
import cairosvg

from truchet_tiling.core.utils import int_to_hex_color

patterns = Pattern()

class Renderer:
    def __init__(self, ctx: Context, cell_size: int, stroke_color: int, stroke_width: int):
        if stroke_color < 0 or stroke_color > 0xffffff:
            raise ValueError(f"Invalid stroke_color value {stroke_color}")
        if stroke_width < 0:
            raise ValueError(f"Invalid stroke_width value {stroke_width}")
        self.ctx = ctx
        self.cell_size = cell_size
        self.stroke_color = stroke_color
        self.stroke_width = stroke_width

    def draw(self, tile:Tile):
        x = tile.x
        y = tile.y
        s = tile.size
        screen_size = s * self.cell_size
        svg_data = patterns.get(s, tile.type)
        for i, stroke in enumerate(tile.strokes):
            color_name = f'{{fill{i}}}'
            new_color = int_to_hex_color(stroke.color) if stroke.color else "#ffffff"
            svg_data = svg_data.replace(color_name, new_color)
            svg_data = svg_data.replace(r"{stroke}", int_to_hex_color(self.stroke_color))
            svg_data = svg_data.replace(r"{stroke-width}", str(self.stroke_width))
        bytes = cairosvg.svg2png(bytestring=svg_data,
                                output_height=screen_size,
                                output_width=screen_size,)  
        surface = ImageSurface.create_from_png(BytesIO(bytes))
        self.ctx.save()
        self.ctx.translate(x * self.cell_size + (s * self.cell_size) / 2, y * self.cell_size + (s * self.cell_size) / 2)
        self.ctx.rotate(tile.rotation)
        self.ctx.translate(-(s * self.cell_size) / 2, -(s * self.cell_size) / 2)
        self.ctx.set_source_surface(surface, 0, 0)
        self.ctx.paint()
        self.ctx.restore()

    def demo_draw(self, tile:DemoTile):
        x = tile.x
        y = tile.y
        s = tile.size
        colors = tile.matrix
        # draw white quadrat with black border in cairo context ctx
        # iterate through 2d numpy array and draw rectangles

        # 1. draw outlines of rectangles
        self.ctx.set_source_rgb(1, 1, 1)  # set the color to black
        self.rectangle(x * self.cell_size, y * self.cell_size, s * self.cell_size, s * self.cell_size)
        self.ctx.stroke()  # draw the outline of the rectangle

        # 2. draw the rectangles
        matrix = tile.matrix._data
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                value = colors._data[i][j]
                color = (2*value + 1)/2
                self.ctx.set_source_rgb(color, color, color)
                self.ctx.rectangle((x + i) * self.cell_size, (y + j) * self.cell_size, self.cell_size, self.cell_size)
                self.ctx.fill()