import math


def rotate_vector(coordinates, angle):
    """Rotates pair of coordinates by a given angle (in degrees counterclockwise)"""
    x, y = adapt_coordinates(*coordinates)
    new_x = math.cos(math.radians(angle)) * x - math.sin(math.radians(angle)) * y
    new_y = math.sin(math.radians(angle)) * x + math.cos(math.radians(angle)) * y

    return adapt_coordinates(new_x, new_y)


def adapt_coordinates(x, y):
    """Since pygame uses different coordinates system than maths, there's need to adapt them"""
    return x, -y
