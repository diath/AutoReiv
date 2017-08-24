import asyncio
import json
import requests

from autoreiv import BasePlugin
from autoreiv import config

class Plugin(BasePlugin):
    def __init__(self):
        super().__init__({
            'name': 'Wordnik',
            'command': 'define',
            'req_params': True,
        })

    @asyncio.coroutine
    def callback(self, bot, msg, data):
        req = requests.get('http://api.wordnik.com/v4/word.json/{}/definitions?api_key={}&limit=3'.format(
            data.get('param'), config.get('tokens').get('wordnik')
        ))
        if req.status_code != 200:
            yield from bot.reply(msg, 'Invalid reply from the server.')
        else:
            info = json.loads(req.text)
            if not info:
                yield from bot.reply(msg, 'No definitions for {}.'.format(data.get('param')))
            else:
                message = 'Definitions for "{}":'.format(data.get('param'))
                for (index, elem, ) in enumerate(info):
                    message += '\n {}) {}'.format(index + 1, elem.get('text'))

                yield from bot.reply(msg, message)
