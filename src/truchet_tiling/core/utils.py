import random
import string
from PIL import Image
import cairo
from cairo import ImageSurface
from io import BytesIO
from itertools import combinations

alphabet = string.ascii_lowercase + string.digits

def random_uuid():
    return ''.join(random.choices(alphabet, k=8))

def select_two(obj, test_func):
    responce = []
    stored_keys = []
    for a, b in combinations(obj.keys(), 2):
        va, vb = obj[a], obj[b]
        if test_func(va, vb) and a not in stored_keys and b not in stored_keys:
            stored_keys.extend([a, b])
            responce.append({a: va, b: vb})
    return responce

def divide_surface(l, s, m, max_cells):
    k = l // s + 1
    k = (k // m + 1) * m if k % m != 0 else k
    return k if k < max_cells else max_cells

def int_to_hex_color(value: int) -> str:
    if not (0x000000 <= value <= 0xFFFFFF):
        raise ValueError("Value must be in the range 0x000000 to 0xFFFFFF")
    return f"#{value:06X}"

def cairo_to_png(surface: ImageSurface) -> BytesIO:
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
    
def close(a, b, tolerance):
    return abs(a - b) < tolerance