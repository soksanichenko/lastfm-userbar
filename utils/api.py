# coding: utf-8
# developed by Stepan Oksanichenko

import requests
from datetime import datetime

from config import API_URL


class LastFmException(Exception):
    def __init__(self, message, error_code):
        Exception.__init__(self, message, error_code)
        self.message = message
        self.error_code = error_code


class LastFmApi:
    def __init__(self, api_key, url=API_URL, raw=False):

        self.api_key = api_key
        self.url = url
        self.raw = raw

    def _call_method(self, method_name, data):
        """

        :param method_name: name of called method
        :param data: data for calling method
        :return: obtained info after calling method

        """
        data.update({
            'method': method_name,
            'format': 'json',
            'api_key': self.api_key
        })

        request = requests.get(url=self.url, params=data)
        result = request.json()
        if 'error' in result.keys():
            raise LastFmException(message=result['message'], error_code=result['error'])
        return result

    @staticmethod
    def _get_image(image_data=None, size='medium'):
        """
        Get image from data about image

        :param image_data: data about image
        :param size: size of image

        :return: url to image

        """
        assert image_data is not None, 'image_data should not be equal None'
        url_image = [img for img in image_data if img['size'] == size][0]['#text']

        return url_image


class User(LastFmApi):
    def __init__(self, api_key, url=API_URL, raw=False, username=None):
        LastFmApi.__init__(self, api_key, url, raw)

        assert username is not None, 'User is not defined'
        self.username = username

    def user_get_recent_tracks(self, limit=1, page=1, extended=0, current=False,
                               from_time=None, to_time=None, raw=None):
        """
        User.GetRecentTracks

        :param raw: return raw data
        :param from_time: display tracks after this time (UNIX timestamp)
        :param to_time: display tracks before this time (UNIX timestamp)
        :param current: return only current track
        :param extended: get extended info about tracks
        :param limit: count of return tracks
        :param page: number of result page

        :return: info about recent scrobbled tracks

        """

        method_name = 'User.GetRecentTracks'

        data = {
            'user': self.username,
            'limit': limit,
            'page': page,
            'extended': extended,
        }
        if to_time:
            data['to'] = to_time
        if from_time:
            data['from'] = from_time
        recent_tracks = self._call_method(method_name, data)
        if self.raw or raw:
            return recent_tracks
        result_tracks = {
            'attributes': recent_tracks['recenttracks']['@attr'],
            'recent_tracks': []
        }
        recent_tracks = recent_tracks['recenttracks']['track']
        for track in recent_tracks:
            _track = {
                'track_name': track['name'].title(),
                'album_name': track['album']['#text'].title(),
                'album_image': self._get_image(track['image']),
                'track_url': track['url']
            }
            if track.get('@attr', False) and track['@attr'].get('nowplaying', False):
                _track['now_playing'] = True if track['@attr']['nowplaying'] == 'true' else False
            if extended:
                _track['artist_image'] = self._get_image(track['artist']['image'])
                _track['artist_url'] = track['artist']['url']
                _track['artist_name'] = track['artist']['name'].title()
            else:
                _track['artist_name'] = track['artist']['#text'].title()
            result_tracks['recent_tracks'].append(_track)
        if current:
            result_tracks['recent_tracks'] = result_tracks['recent_tracks'][:len(result_tracks) - 1]
        return result_tracks

    def user_get_info(self, raw=False):
        """User.GetInfo

        :param raw: return raw data

        :return user_data: info about last.fm user

        """

        method_name = 'User.GetInfo'

        data = {
            'user': self.username,
        }

        result = self._call_method(method_name, data)
        user_info = {
            'attributes': result['user']['@attr'],
            'user_info': {}
        }
        if self.raw or raw:
            return result
        if 'user' in result.keys():
            result = result['user']
            user_info['user_info'].update(result)
            user_info['user_info']['image'] = self._get_image(user_info['user_info']['image'])
            user_info['user_info']['registered'] = \
                datetime.fromtimestamp(int(user_info['user_info']['registered']['unixtime'])). \
                strftime('%d-%m-%Y %H:%M:%S')
        return user_info

    def user_get_artist_tracks(self, raw=False, artist=None, from_time=None, to_time=None, page=1):
        """
        User.GetArtistTracks

        :param raw: return raw data
        :param from_time: display tracks after this time (UNIX timestamp)
        :param to_time: display tracks before this time (UNIX timestamp)
        :param page: number of result page
        :param artist: artist name

        :return: scrobbled tracks by artist name

        """

        method_name = 'User.GetArtistTracks'

        assert artist is not None, 'Artist name is not define'
        data = {
            'user': self.username,
            'artist': artist,
            'page': page,
        }
        if from_time:
            data['startTimestamp'] = from_time
        if to_time:
            data['endTimestamp'] = to_time
        result = self._call_method(method_name, data)
        if self.raw or raw:
            return result
