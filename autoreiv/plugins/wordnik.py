import asyncio
import requests
import json

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
            if len(info) == 0:
                yield from bot.reply(msg, 'No definitions for {}.'.format(data.get('param')))
            else:
                message = 'Definitions for "{}":'.format(data.get('param'))
                for x in range(len(info)):
                    message += '\n {}) {}'.format(x + 1, info[x]['text'])

                yield from bot.reply(msg, message)
