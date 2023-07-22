import math
import re
from fractions import Fraction


def check_input(input_string: str):
    if re.search("^\d+\s\d{1,2}/\d{1,2}$", input_string):
        integer = re.search("^\d+\s", input_string).group().rstrip()
        fraction = Fraction(re.search("\s\d{1,2}\/\d{1,2}", input_string).group().lstrip())
        return int(integer) + fraction
    elif re.search("^\d+$", input_string):
        return int(re.search("^\d+$", input_string).group())
    else:
        return False


def construct_triangles(side_lengths: dict):
    triangle_a = [side_lengths["AC"], side_lengths["AB"], side_lengths["BC"]]
    triangle_d = [side_lengths["CD"], side_lengths["BD"], side_lengths["BC"]]
    triangle_b = [side_lengths["AB"], side_lengths["BD"], side_lengths["AD"]]
    triangle_c = [side_lengths["AC"], side_lengths["CD"], side_lengths["AD"]]
    return {"Triangle A": triangle_a, "Triangle B": triangle_b, "Triangle C": triangle_c, "Triangle D": triangle_d}


def calculate_angle(side_lengths: list):
    # Law of Cosines formula : cosA = (a^2 - (b^2 + c^2))/ (-2*b*c)
    a = side_lengths[2]
    b = side_lengths[0]
    c = side_lengths[1]
    cos_a = (a**2 - (c**2 + b**2)) / (-2 * b * c)
    try:
        ans = math.acos(cos_a)
    except ValueError:
        return "Error: Invalid input, your measurements are incorrect"
    return math.degrees(ans)


def calculate_angles(input_dict):
    diagonals = {"AD": check_input(input_dict['diag_ad']), "BC": check_input(input_dict['diag_bc'])}

    sides = {"AB": check_input(input_dict['side_ab']), "CD": check_input(input_dict['side_cd']),
             "AC": check_input(input_dict['side_ac']), "BD": check_input(input_dict['side_bd'])} | diagonals

    triangles = construct_triangles(sides)
    angles = {}
    # Use Law of Cosines in the 4 triangles to solve for the corner angles in the quadrilateral
    for key, value in triangles.items():
        angle = calculate_angle(value)
        if isinstance(angle, str):
            triangle = key.lstrip("Triangle ")
            angles['error'] = angle
            angles[triangle] = "Error"
            continue
        angles[key.lstrip('Triangle ')] = f"{round(angle, 2)}°"

    return angles
