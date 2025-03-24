from math import sin, cos, radians
def find_rotated_point(x1: float, y1: float, angle: float):
    x2 = x1 * cos(radians(angle)) - y1 * sin(radians(angle))
    y2 = x1 * sin(radians(angle)) + y1 * cos(radians(angle))
    return [x2, y2]