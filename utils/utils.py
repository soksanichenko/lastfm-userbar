# coding: utf-8
# developed by Stepan Oksanichenko


def parse_color_string(color):
    """

    Parse color string from url
    :param color: color string
    :return: RGB tuple

    """

    color = color.split('_')
    color = map(lambda item: int(item), color)
    color = tuple(color)

    return color


def hex_to_rgb_string(color):
    """

    Convert hex color to rgb string color

    :param color: hex color
    :return: rgb string color

    """

    color = color.lstrip('#')
    color = [int(color[i:i+2], 16) for i in (0, 2, 4)]
    color = map(lambda item: str(item), color)
    color = '_'.join(color)

    return color


def hex_to_rgb_tuple(color):
    """

    Convert hex color to rgb tuple color

    :param color: hex color
    :return: rgb tuple color

    """

    color = color.lstrip('#')
    color = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))

    return color
