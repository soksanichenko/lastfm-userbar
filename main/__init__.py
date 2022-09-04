# coding: utf-8
# developed by Stepan Oksanichenko
# developed at 02.05.2018 22:09

import os

from flask import Blueprint

lastfm_app = Blueprint(
    'lastfm_app',
    __name__,
    template_folder=os.path.join('..', 'templates'),
    static_folder=os.path.join('..', 'static'),
)

from . import forms, views
