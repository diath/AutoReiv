import asyncio
import wolframalpha

from autoreiv import BasePlugin
from autoreiv import config

class Plugin(BasePlugin):
    def __init__(self):
        super().__init__({
            'name': 'Calculator',
            'command': 'calc',
            'req_params': True,
        })

        self.client = wolframalpha.Client(config.get('tokens').get('wolfram'))

    @asyncio.coroutine
    def callback(self, bot, msg, data):
        try:
            res = self.client.query(data.get('param'))
        except:
            yield from bot.reply(msg, 'Invalid reply from the server.')
        finally:
            yield from bot.reply(msg, '{}'.format(next(res.results).text))
