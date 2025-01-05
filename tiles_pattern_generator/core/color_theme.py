import random
from core.commons.enums import Theme


class ColorTheme:
    def __init__(self, theme:Theme = None):
        random_colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(10)]
        self.colors ={
            Theme.GREEN: ['#2B450E', '#ABCE86', '#79C429', '#456423', '#5A911F'],
            Theme.MORDOR: ['#E63946', '#FF5733', '#5A5A5A', '#1C1C1C', '#DAA520', '#333333', '#222222', '#111111', '#8B0000'],
            Theme.RANDOM: ['#%02X%02X%02X' % tuple(color) for color in random_colors]
        }
        self.theme = theme

    @property
    def random_color(self) -> list:
        return random.choice(self.colors[self.theme])