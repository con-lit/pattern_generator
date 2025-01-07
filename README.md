# A truchet tiles generator

Creates a truchet pattern as a PNG bitmap.

![](https://raw.githubusercontent.com/con-lit/pattern_generator/refs/heads/main/examples/images/pattern01.png)

## Install

`pip install truchet-tiling`

## Usage

```python
import truchet_tiling.truchet_pattern as tp
from truchet_tiling.themes import RED_FLAMES 

image = tp.generate(
    width=700,
    height=500,
    colors = RED_FLAMES,
    directions='mixed',
    arcs_probability=1,
    stroke_color=0xFFFFFF,
    stroke_width=6
)
```

To try it in Jupyter Notebook:

```python
import truchet_tiling.truchet_pattern as tp

# helper to display bitmap images
def display_image(image_bytes):
  from IPython.display import display, Image as IPImage
  display(IPImage(data=image_bytes.getvalue()))

image = tp.generate(width=800, height=600)
display_image(image)
```

Parameters:  
**width (int)**: Minimal width of the pattern.  
**height (int)**: Minimal height of the pattern.  
**cell_size (int)**: Size of the cell in the pattern.  
**arcs_probability (float)**: Probability of arcs in the pattern. Accepted float values in the range [0, 1].  
**directions (str)**: Direction of the pattern. Accepted values are ['mixed', 'horizontal', 'vertical'].  
**colors (List[int])**: List of colors to use in the pattern. With Null a random color set will be used.  
**stroke_color (int)**: Color of the strokes.  
**stroke_width (int)**: Width of the strokes.  
