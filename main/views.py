# coding: utf-8
# developed by Stepan Oksanichenko
from urllib.parse import parse_qsl, quote

from flask import send_file, request, render_template

from main import lastfm_app
from main.forms import Generator, Generator2
from utils.main import create_userbar, create_userbar2
from utils.nocache import nocache
from utils.utils import parse_color_string, hex_to_rgb_string, hex_to_rgb_tuple


colors_data = [
    'inner_color', 'outer_color', 'text_color', 'border_color', 'logo_color', 'ic', 'oc', 'tc', 'bc', 'lc',
]


@lastfm_app.route('/format1.html', methods=['GET', 'POST'])
def generator():
    form = Generator()
    data = {
        'title': 'Generator #1 Last.Fm UserBar',
        'page_title': 'Generator #1 Last.Fm UserBar',
        'form': form,
    }
    if form.validate_on_submit():
        result = request.url_root
        result = '{}{}/'.format(result, form.data['username'])
        params = ['{}={}'.format(key, hex_to_rgb_string(value)) for key, value in form.data.items()
                  if key in colors_data and value]
        if 'truncate_text' in form.data.keys():
            params.append('truncate_text={}'.format(form.data['truncate_text']))
        params = '&'.join(params)
        params = quote(params)
        result = '{}{}/'.format(result, params)
        result = '{}{}'.format(result, 'userbar.png')
        data['result'] = result
    return render_template('format1.html', **data)


@lastfm_app.route('/format2.html', methods=['GET', 'POST'])
def generator2():
    form = Generator2()
    data = {
        'title': 'Generator Last.Fm UserBar',
        'page_title': 'Generator Last.Fm UserBar',
        'form': form,
    }
    if form.validate_on_submit():
        result = request.url_root
        result = '{}{}/'.format(result, form.data['username'])
        params = ['{}={}'.format(key, value) for key, value in form.data.items()
                  if key in colors_data and value]
        if 'tt' in form.data.keys():
            params.append('tt={}'.format(form.data['tt']))
        params = '&'.join(params)
        params = quote(params)
        result = '{}{}/'.format(result, params)
        result = '{}{}'.format(result, 'userbar2.png')
        data['result'] = result
    return render_template('format2.html', **data)


@lastfm_app.route('/')
@nocache
def main():
    data = {
        'title': 'Last.Fm UserBar',
        'page_title': 'Last.Fm UserBar',
        'root_url': request.url_root,
    }
    return render_template('main.html', **data)


@lastfm_app.route('/<username>/<inner_color>/<outer_color>/<text_color>/userbar.png')
@nocache
def user_bar(username, inner_color, outer_color, text_color):
    inner_color = parse_color_string(inner_color)
    outer_color = parse_color_string(outer_color)
    text_color = parse_color_string(text_color)
    img = create_userbar(username, inner_color, outer_color, text_color)
    img.seek(0)
    return send_file(img, mimetype='image/png')


@lastfm_app.route('/<username>/userbar.png')
@lastfm_app.route('/<username>/<params>/userbar.png')
@nocache
def new_user_bar(username, params=None):
    img_data = {
        'inner_color': (0, 0, 0,),
        'logo_color': None,
        'outer_color': (255, 255, 255,),
        'text_color': (255, 255, 255,),
        'border_color': None,
        'truncate_text': False,
    }
    if params:
        query = dict(parse_qsl(params))
        for key, value in query.items():
            if key in colors_data:
                if value != 'None' and key != 'truncate_text':
                    query[key] = parse_color_string(value)
                elif key == 'truncate_text':
                    query[key] = True if value == 'True' else False
                else:
                    query[key] = img_data[key]
        img_data.update(query)
    img = create_userbar(username, **img_data)
    img.seek(0)

    return send_file(img, mimetype='image/png')


@lastfm_app.route('/<username>/userbar2.png')
@lastfm_app.route('/<username>/<params>/userbar2.png')
@nocache
def new_user_bar2(username, params=None):
    img_data = {
        'ic': (0, 0, 0,),
        'lc': None,
        'oc': (255, 255, 255,),
        'tc': (255, 255, 255,),
        'bc': None,
        'tt': False,
    }
    if params:
        query = dict(parse_qsl(params))
        for key, value in query.items():
            if key in colors_data:
                if value != 'None' and key != 'tt':
                    query[key] = hex_to_rgb_tuple(value)
            elif key == 'tt':
                query[key] = True if value == 'True' else False
            else:
                query[key] = img_data[key]
        img_data.update(query)
    img = create_userbar2(username, **img_data)
    img.seek(0)

    return send_file(img, mimetype='image/png')
