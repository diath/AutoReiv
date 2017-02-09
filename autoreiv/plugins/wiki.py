import asyncio
import wikipedia

from autoreiv import BasePlugin

class Plugin(BasePlugin):
    def __init__(self):
        super().__init__()
        self.name = 'Wikipedia'
        self.command = 'wiki'
        self.reqParams = True

    @asyncio.coroutine
    def callback(self, bot, msg, data):
        summary = wikipedia.summary(data.get('param'), sentences=3)
        if len(summary) > 250:
            summary = '{}...'.format(summary[:247])

        yield from bot.reply(msg, '{} (More at https://wikipedia.org/wiki/{})'.format(
            summary.replace('\n', ''), data.get('param').replace(' ', '%20')
        ))
