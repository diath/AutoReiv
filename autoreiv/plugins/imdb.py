import asyncio
import requests
import json

from autoreiv import BasePlugin

class Plugin(BasePlugin):
    def __init__(self):
        super().__init__({
            'name': 'IMDb',
            'command': 'imdb',
            'req_params': True,
        })

    @asyncio.coroutine
    def callback(self, bot, msg, data):
        req = requests.get('http://omdbapi.com/?t={}'.format(data.get('param')))
        if req.status_code != 200:
            yield from bot.reply(msg, 'Invalid reply from the server.')
        else:
            info = json.loads(req.text)
            if info.get('Error'):
                yield from bot.reply(msg, '{}'.format(info.get('Error')))
            else:
                yield from bot.reply(msg, '{} ({}) ({}), more at http://imdb.com/title/{}'.format(
                    info['Title'], info['Year'],
                    info['Genre'], info['imdbID']
                ))
