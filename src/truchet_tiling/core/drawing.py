import svgwrite

class Drawing:
    def __init__(self, width:int, height:int):
        self.width = width
        self.height = height
        self.svg = svgwrite.Drawing(size=("100%", "100%"))
        self.svg.viewbox(*[0, 0, width, height])

    def save(self, filename:str):
        self.svg.saveas(filename)
    
    def add(self, element):
        self.svg.add(element)