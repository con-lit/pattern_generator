import svgwrite

from truchet_tiling.core.drawing_model import DrawingModel

class Drawing:
    def __init__(self, width:int, height:int, model:DrawingModel):
        self.width = width
        self.height = height
        self.model = model
        self.svg = svgwrite.Drawing(size=("100%", "100%"))
        self.svg.viewbox(*[0, 0, width, height])

    def save(self, filename:str):
        for id, path in self.model.lines.items():
            path_string = path.d()
            path_element = svgwrite.path.Path(
                d=path_string,
                stroke="black",
                fill="none",
                stroke_width=1,
                id=id
            )
            self.svg.add(path_element)
        self.svg.saveas(filename)