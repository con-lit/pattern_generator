from io import BytesIO
from typing import List, Literal

from cairo import FORMAT_ARGB32, Context, ImageSurface
from src import themes
from src.truchet_tiling.core.commons.constants import MAX_QUAD_SIZE
from src.truchet_tiling.core.connector import Connector
from src.truchet_tiling.core.renderer import Renderer
from src.truchet_tiling.core.fills.perlin import Perlin
from src.truchet_tiling.core.generators import ColorGenerator, DesignGenerator
from src.truchet_tiling.core.quadtree import QuadTree
from src.truchet_tiling.core.utils import cairo_to_png, divide_surface

    
def generate(
        width:int = 800,
        height:int = 600,
        cell_size:int = 40,
        arcs_probability:float = 0.5,
        directions:Literal['mixed', 'horizontal', 'vertical'] = 'mixed',
        colors:List[int] = themes.RANDOM,
        stroke_color: int = 0x000000,
        stroke_width: int = 8,
    ) -> BytesIO:
    """
    Generate a truchet pattern.

    Parameters:
    width (int): Minimal width of the pattern.
    height (int): Minimal height of the pattern.
    cell_size (int): Size of the cell in the pattern.
    arcs_probability (int): Probability of arcs in the pattern.
    directions (str): Direction of the pattern. Accepted values are ['mixed', 'horizontal', 'vertical'].
    colors (List[int]): List of colors to use in the pattern. With Null a random color set will be used.

    Returns:
    Image: Generated truchet pattern image.
    """

    size_width = divide_surface(width, cell_size, MAX_QUAD_SIZE, 36)
    size_height = divide_surface(height, cell_size, MAX_QUAD_SIZE, 24)

    quadtree = QuadTree((0, 0, size_width, size_height),
                        matrix = Perlin(size_width, size_height, octaves=3),
                        connector = Connector(size_width,
                                              size_height,
                                              DesignGenerator(arcs_probability, directions)))
    quadtree.connect()
    quadtree.colorize(ColorGenerator(colors))

    surface = ImageSurface(FORMAT_ARGB32, size_width*cell_size, size_height*cell_size)
    quadtree.render(Renderer(Context(surface), cell_size, stroke_color, stroke_width))

    img = cairo_to_png(surface)
    return img