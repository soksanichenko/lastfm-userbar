# coding: utf-8
# developed by Stepan Oksanichenko
from functools import wraps, update_wrapper

from flask import make_response


def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return response

    return update_wrapper(no_cache, view)
