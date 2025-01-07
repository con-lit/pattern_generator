# A truchet tiles generator

Creates a truchet pattern as a PNG bitmap.

![](https://raw.githubusercontent.com/con-lit/pattern_generator/refs/heads/main/examples/images/pattern01.png)

## Install

`pip install truchet-tiling`

## Usage

```python
import truchet_tiling.truchet_pattern as tp
from truchet_tiling.themes import BLUE_WAVES, RED_FLAMES, GREEN_FIELDS 

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
