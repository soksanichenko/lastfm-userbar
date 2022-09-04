# coding: utf-8
# developed by Stepan Oksanichenko
import os
from io import BytesIO
from config import LASTFM_API_KEY, PATH_TO_FONT
from PIL import Image, ImageFont, ImageDraw

from .api import LastFmException, User

from main import lastfm_app


def user_get_last_track(username=None):
    """Get user last track

    :param username: last.fm username

    :return last_track: user last track

    """
    result = None
    last_track = None
    user = User(LASTFM_API_KEY, username=username) or None
    try:
        result = user.user_get_recent_tracks(extended=1)
        result = result['recent_tracks']
    except LastFmException as error:
        last_track = error.message
    if not result and not last_track:
        last_track = 'Not recent tracks'
    elif isinstance(result, list):
        last_track = [track for track in result if track.get('now_playing')]
        if not last_track:
            last_track = result
        last_track = dict(last_track[0])

    return last_track


def gradient(inner_color, outer_color, border_color=None, width=350):
    """
    Create user bar with gradient

    :param inner_color: start color
    :param outer_color: end color
    :param border_color: color of border
    :param width: width of userbar

    :return: BytesIO with img

    """

    def interpolate(f_co, t_co, interval):
        det_co = [(t - f) / interval for f, t in zip(f_co, t_co)]
        for i in range(interval):
            yield [round(f + det * i) for f, det in zip(f_co, det_co)]

    img_size = (width, 23)
    image = Image.new('RGBA', img_size, color=0)
    draw = ImageDraw.Draw(image)

    for i, color in enumerate(interpolate(inner_color, outer_color, image.width)):
        draw.line([(i, 0), (i, image.height)], tuple(color), width=1)

    if border_color is not None:
        invert_border_color = tuple(map(lambda item: 255 - int(item), border_color))
        draw.line([(0, 0), (image.width - 1, 0)], border_color, width=1)
        draw.line([(0, image.height - 1), (image.width - 1, image.height - 1)], border_color, width=1)
        draw.line([(0, 0), (0, image.height - 1)], width=1, fill=border_color)
        draw.line([(image.width - 1, 0), (image.width - 1, image.height - 1)], width=1, fill=border_color)
        draw.line([(1, 1), (image.width - 2, 1)], width=1, fill=invert_border_color)
        draw.line([(1, image.height - 2), (image.width - 2, image.height - 2)], width=1, fill=invert_border_color)
        draw.line([(1, 1), (1, image.height - 2)], width=1, fill=invert_border_color)
        draw.line([(image.width - 2, 1), (image.width - 2, image.height - 2)], width=1, fill=invert_border_color)
    out_img = BytesIO()
    image.save(out_img, 'PNG')
    out_img.seek(0)

    return out_img


def paste_text(text, text_color, inner_color, outer_color, border_color, truncate_text=False):
    """
    Paste text on img

    :param truncate_text: truncate userbar text
    :param text: text for pasting
    :param inner_color: start color for BG
    :param outer_color: end color for BG
    :param text_color: color of paste text
    :param border_color: color of border

    :return: BytesIO with img

    """
    default_width = 305
    max_width = 750
    trunc_value = 70
    in_img = gradient(inner_color, outer_color, border_color, width=default_width)
    trunc_len = 95
    x, y = 10, 2
    in_img.seek(0)
    img = Image.new('RGBA', (1, 1,))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(os.path.join(lastfm_app.static_folder, PATH_TO_FONT), 14, encoding='utf-8')
    text_width, _ = draw.textsize(text, font)
    if truncate_text:
        bar_width = min(max_width, trunc_value + text_width)
        text = '{}...'.format(text[:trunc_len]) if len(text) > trunc_len else text
    else:
        bar_width = max(default_width, trunc_value + text_width)
    in_img = gradient(inner_color, outer_color, border_color, width=bar_width)
    in_img.seek(0)
    img = Image.open(in_img)
    draw = ImageDraw.Draw(img)
    draw.text((x, y), text, font=font, fill=text_color)
    out_img = BytesIO()
    img.save(out_img, 'PNG')
    out_img.seek(0)

    return out_img


def paste_logo(in_img, logo_color=None):
    """
    Paste logo to userbar
    :param in_img: BytesIO with img
    :param logo_color: color of logo


    :return: BytesIO with img

    """

    if logo_color is None:
        return in_img

    logo = Image.open(os.path.join(lastfm_app.static_folder, 'logo.png'))
    in_img.seek(0)
    img = Image.open(in_img)
    for x in range(logo.size[0]):
        for y in range(logo.size[1]):
            pixel = logo.getpixel((x, y))
            if pixel[3] > 0:
                out_pixel = list(logo_color)
                out_pixel.append(pixel[3])
                out_pixel = tuple(out_pixel)
                logo.putpixel((x, y), out_pixel)
    out_img = BytesIO()
    width, height = img.size
    img.paste(logo, (width - 40, 3), logo)
    img.save(out_img, 'PNG')
    out_img.seek(0)

    return out_img


def make_userbar_text(text_format='{artist_name} - {track_name}', **kwargs):
    """
    Make userbar text
    :param text_format: text format
    :param kwargs: key for formatting text
    :return: userbar text
    """

    out_text = text_format.format(**kwargs)

    return out_text


def create_userbar(username, inner_color, outer_color, text_color, border_color=None, logo_color=None,
                   truncate_text=False):
    """

    Create user bar

    :param truncate_text: truncate userbar text
    :param border_color: color of border
    :param username: lastfm_app username
    :param inner_color: start color for BG
    :param outer_color: end color for BG
    :param text_color: color of paste text
    :param logo_color: color of logo

    :return: BytesIO with img

    """

    result = user_get_last_track(username=username)
    if isinstance(result, dict):
        text = make_userbar_text(**result)
    else:
        text = result
    print(text)
    img = paste_text(text, text_color, inner_color, outer_color, border_color, truncate_text)
    img.seek(0)
    if logo_color is not None:
        img = paste_logo(img, logo_color)

    return img


def create_userbar2(username, ic, oc, tc, bc=None, lc=None, tt=False):
    """

    Create user bar

    :param tt: truncate userbar text
    :param bc: color of border
    :param username: lastfm_app username
    :param ic: start color for BG
    :param oc: end color for BG
    :param tc: color of paste text
    :param lc: color of logo

    :return: BytesIO with img

    """
    result = user_get_last_track(username=username)
    if isinstance(result, dict):
        text = make_userbar_text(**result)
    else:
        text = result
    print(text)
    img = paste_text(text, tc, ic, oc, bc, tt)
    img.seek(0)
    if lc is not None:
        img = paste_logo(img, lc)

    return img
