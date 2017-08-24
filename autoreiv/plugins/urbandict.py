import asyncio
import json
import requests

from autoreiv import BasePlugin

class Plugin(BasePlugin):
    def __init__(self):
        super().__init__({
            'name': 'Urban Dictionary',
            'command': 'ud',
            'req_params': True,
        })

    @asyncio.coroutine
    def callback(self, bot, msg, data):
        req = requests.get('http://api.urbandictionary.com/v0/define?page=0&term={}'.format(
            data.get('param')
        ))
        if req.status_code != 200:
            yield from bot.reply(msg, 'Invalid reply from the server')
        else:
            info = json.loads(req.text).get('list')
            if not info:
                yield from bot.reply(msg, 'No definitions found.')
            else:
                message = 'Definitions for "{}":'.format(data.get('param'))
                for index in range(min(len(info), 3)):
                    message += '\n {}) {}'.format(index + 1, info[index]['definition'])

                yield from bot.reply(msg, message)
