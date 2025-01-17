import math
from typing import Literal
from svgpathtools import Line, CubicBezier, Path, svg2paths
import svgwrite.path
from xml.etree import ElementTree as ET

from truchet_tiling.core.utils import close

def transform_complex_point(z, sx, sy, angle_degrees, tx, ty):
    """
    Applies scale, rotation, and translation to a complex coordinate z.

    :param z: complex number representing the original point (x + y*i).
    :param sx: scale factor in the x-direction.
    :param sy: scale factor in the y-direction.
    :param angle_degrees: rotation angle in degrees (counterclockwise).
    :param tx: translation in the x-direction.
    :param ty: translation in the y-direction.
    :return: transformed complex number (x' + y'*i).
    """
    # 1) Scale
    x_scaled = z.real * sx
    y_scaled = z.imag * sy
    z_scaled = complex(x_scaled, y_scaled)

    # 2) Rotate
    # Convert degrees to radians
    angle_radians = math.radians(angle_degrees)
    # Multiply by e^(i * angle)
    z_rotated = z_scaled * complex(math.cos(angle_radians), math.sin(angle_radians))

    # 3) Translate
    x_final = z_rotated.real + tx
    y_final = z_rotated.imag + ty

    return complex(x_final, y_final)

def translate_path(path, tx=0, ty=0, sx=1, sy=1, r=0) -> Path:
    new_segments = []
    for segment in path:
        new_segment = segment
        if isinstance(segment, Line):
            start = segment.start
            end = segment.end
            new_start = transform_complex_point(start, sx, sy, r, tx, ty)
            new_end = transform_complex_point(end, sx, sy, r, tx, ty)
            new_segment = Line(new_start, new_end)
        elif isinstance(segment, CubicBezier):
            start = segment.start
            control1 = segment.control1
            control2 = segment.control2
            end = segment.end
            new_start = transform_complex_point(start, sx, sy, r, tx, ty)
            new_control1 = transform_complex_point(control1, sx, sy, r, tx, ty)
            new_control2 = transform_complex_point(control2, sx, sy, r, tx, ty)
            new_end = transform_complex_point(end, sx, sy, r, tx, ty)
            new_segment = CubicBezier(new_start, new_control1, new_control2, new_end)
        new_segments.append(new_segment)
    return Path(*new_segments)

def get_triangles_translation(r: Literal[0, 120, 240], width, height, scale_x=1, scale_y=1):
    match r:
        case 120:
            tx=width if (scale_x == 1 and scale_y == 1) else width/2
            ty=0 if scale_x == 1 else height
        case 240:
            tx=width/2
            if (scale_x == -1 and scale_y == 1): tx=0
            if (scale_x == 1 and scale_y == -1): tx=width
            ty=height if scale_x == 1 else 0
        case 0:
            tx=0 if scale_x == 1 else width
            ty=0 if scale_y == 1 else height
    return tx,ty

def create_svg(input:str, rotation:Literal[0, 120, 240]=0, scale_x:int=1, scale_y:int=1):
    tree = ET.parse(input)
    root = tree.getroot()

    width = root.get('width', '100%')
    height = root.get('height', '100%')
    view_box = root.get('viewBox', '0 0 100 100')
    vb_x, vb_y, vb_width, vb_height = map(float, view_box.split())

    dwg = svgwrite.Drawing(size=(width, height))
    dwg.viewbox(*[vb_x, vb_y, vb_width, vb_height])

    paths, attributes = svg2paths(input)
    for a in attributes:
        print(a)
    print('---')

    for path in paths:
        print(path)
        tx, ty = get_triangles_translation(rotation, vb_width, vb_height, scale_x, scale_y)
        translated_path = translate_path(path, r=rotation, tx=tx, ty=ty, sx=scale_x, sy=scale_y)
        path_string = translated_path.d()
        path_element = svgwrite.path.Path(
            d=path_string,
            stroke="black",
            fill="none",
            stroke_width=1
        )
        dwg.add(path_element)

    return dwg.tostring()

def connect_pathes(p1: Path, p2: Path, tolerance=0.1):
    s1, e1 = p1.start, p1.end
    s2, e2 = p2.start, p2.end

    if close(e1, s2, tolerance):
        p2.start = e1
        first, second = p1, p2
    elif close(e2, s1, tolerance):
        p1.start = e2
        first, second = p2, p1
    elif close(s1, s2, tolerance):
        p1.start = s2
        first, second = p1.reversed(), p2
    elif close(e1, e2, tolerance): 
        p1.end = e2
        first, second = p1, p2.reversed()
    else:
        first, second = p1, p2
    
    seg1 = first[-1]
    seg2 = second[0]
    d1 = seg1.derivative(1.0)
    d2 = seg2.derivative(0.0)
    print(abs(d1 - d2) < 0.2)
    return Path(*first, *second)
    