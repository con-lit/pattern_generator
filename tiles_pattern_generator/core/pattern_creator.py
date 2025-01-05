from PIL import Image
import cairo
from cairo import ImageSurface, FORMAT_ARGB32, Context
from core.color_theme import ColorTheme
from core.connector import Connector
from core.draw import draw
from core.fills.perlin import Perlin
from core.quadtree import QuadTree
from core.commons.constants import SHAPE, TILE_SIZE
from io import BytesIO
from core.commons.enums import Design, Direction, Theme

def divide_surface(l, s, m):
    k = l // s + 1
    k = (k // m + 1) * m if k % m != 0 else k
    return k

def cairo_to_image(surface: ImageSurface) -> BytesIO:
    format = surface.get_format()
    size = (surface.get_width(), surface.get_height())
    stride = surface.get_stride()

    with surface.get_data() as memory:
        if format == cairo.Format.RGB24:
            img = Image.frombuffer(
                "RGB", size, memory.tobytes(),
                'raw', "BGRX", stride)
        elif format == cairo.Format.ARGB32:
            img = Image.frombuffer(
                "RGBA", size, memory.tobytes(),
                'raw', "BGRa", stride)
        else:
            raise NotImplementedError(repr(format))
        buf = BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        return buf

def truchet_tiles(width:int, hight:int, design:Design, direction:Direction, theme:Theme) -> BytesIO:
    k_width = divide_surface(width, TILE_SIZE, SHAPE)
    k_hight = divide_surface(hight, TILE_SIZE, SHAPE)

    if k_width > 36:
        k_width = 36

    if k_hight > 24:
        k_hight = 24

    quadtree = QuadTree((0, 0, k_width, k_hight),
                        matrix = Perlin(k_width, k_hight, octaves=3),
                        connector = Connector(k_width,
                                              k_hight,
                                              design = design,
                                              direction = direction))
    quadtree.connect()
    quadtree.colorize(ColorTheme(theme))

    surface = ImageSurface(FORMAT_ARGB32, k_width*TILE_SIZE, k_hight*TILE_SIZE)
    ctx = Context(surface)
    quadtree.render(ctx, draw)

    img = cairo_to_image(surface)
    return img