# coding: utf-8
# developed by Stepan Oksanichenko

import wtforms.validators as validators
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.widgets import Input

from utils.api import LastFmException, User
from config import LASTFM_API_KEY


def username_validate(form, field):
    print('validate form: ', form, '\n', 'validate field: ', field)
    username = field.data
    user = User(LASTFM_API_KEY, username=username)
    try:
        user.user_get_recent_tracks(extended=1)
    except LastFmException as error:
        field.errors.append('{}'.format(error.message))
        raise validators.StopValidation()


class Generator(FlaskForm):
    username = StringField('Username', validators=[username_validate], default='ZelGray')
    inner_color = StringField('Inner color', validators=[validators.DataRequired()], widget=Input(input_type='color'),
                              default='#000000')
    outer_color = StringField('Outer color', validators=[validators.DataRequired()], widget=Input(input_type='color'),
                              default='#FFFFFF')
    text_color = StringField('Text color', validators=[validators.DataRequired()], widget=Input(input_type='color'),
                             default='#FFFFFF')
    border_color = StringField('Border color', widget=Input(input_type='color'),
                               default='#000000')
    enable_border = BooleanField('Enable border', default=False)
    logo_color = StringField('Logo color', widget=Input(input_type='color'),
                             default='#000000')
    truncate_text = BooleanField('Truncate image (to 750px)', default=False)
    enable_logo = BooleanField('Enable logo', default=False)


class Generator2(FlaskForm):
    username = StringField('Username', validators=[username_validate], default='ZelGray')
    ic = StringField('Inner color', validators=[validators.DataRequired()], widget=Input(input_type='color'),
                     default='#000000')
    oc = StringField('Outer color', validators=[validators.DataRequired()], widget=Input(input_type='color'),
                     default='#FFFFFF')
    tc = StringField('Text color', validators=[validators.DataRequired()], widget=Input(input_type='color'),
                     default='#FFFFFF')
    bc = StringField('Border color', widget=Input(input_type='color'),
                     default='#000000')
    eb = BooleanField('Enable border', default=False)
    lc = StringField('Logo color', widget=Input(input_type='color'),
                     default='#000000')
    tt = BooleanField('Truncate image (to 750px)', default=False)
    el = BooleanField('Enable logo', default=False)
