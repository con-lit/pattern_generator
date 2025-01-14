from math import floor
from truchet_tiling.core.generators import ColorGenerator
from truchet_tiling.commons.constants import MAX_QUAD_SIZE
from truchet_tiling.core.connector import Connector
from truchet_tiling.fills.perlin import Perlin
from truchet_tiling.core.renderer import Renderer
from truchet_tiling.core.tile import Tile


class QuadTree:
    def __init__(self,
                 boundary:tuple,
                 matrix:Perlin,
                 connector: Connector):
        self.boundary = boundary
        self.matrix = matrix
        self.connector = connector
        if self.can_be_divided:
            if self.boundary[2] > MAX_QUAD_SIZE and self.boundary[3] > MAX_QUAD_SIZE:
                self._divide_surface()
            else:
                self._divide_quads()
        else:
            self.children = []
            self.tile = Tile(x=boundary[0],
                             y=boundary[1],
                             size=boundary[2],
                             connector=connector)

    @property
    def can_be_divided(self):
        return self.boundary[2] > 1 and self.boundary[3] > 1 and self.matrix.max >0
    
    @property
    def divided(self):
        return bool(self.children)
    
    def _divide_surface(self):
        k_width = self.boundary[2]
        k_hight = self.boundary[3]
        self.children = []
        for y in range(0, k_hight, MAX_QUAD_SIZE):
            for x in range(0, k_width, MAX_QUAD_SIZE):
                boundary = (x, y, MAX_QUAD_SIZE, MAX_QUAD_SIZE)
                self.children.append(QuadTree(boundary,
                                              self.matrix.slice(x=boundary[0],
                                                                y=boundary[1],
                                                                size=boundary[2]),
                                              self.connector))

    def _divide_quads(self):
        x, y, s, s = self.boundary
        s_2 = floor(s / 2)
        nw = (x, y, s_2, s_2)
        ne = (x + s_2, y, s_2, s_2)
        sw = (x, y + s_2, s_2, s_2)
        se = (x + s_2, y + s_2, s_2, s_2)
        nw_slice = self.matrix.slice(0, 0, s_2)
        ne_slice = self.matrix.slice(s_2, 0, s_2)
        sw_slice = self.matrix.slice(0, s_2, s_2)
        se_slice = self.matrix.slice(s_2, s_2, s_2)
        self.children = [
            QuadTree(nw, nw_slice, self.connector),
            QuadTree(ne, ne_slice, self.connector),
            QuadTree(sw, sw_slice, self.connector),
            QuadTree(se, se_slice, self.connector),
        ]

    def render(self, renderer:Renderer):
        if self.divided:
            for child in self.children: child.render(renderer)
        else:
            renderer.draw(self.tile)

    def connect(self):
        if self.divided:
            for child in self.children: child.connect()
        else:
            self.tile.connect()

    def colorize(self, color_generator:ColorGenerator):
        if self.divided:
            for child in self.children: child.colorize(color_generator)
        else:
            for stroke in  self.tile.strokes:
                stroke.set_color(color_generator.random_color)
