import asyncio

class BasePlugin(object):
    def __init__(self, data):
        self.name = data.get('name', 'Unknown')
        self.command = data.get('command', None)
        self.pattern = data.get('pattern', None)
        self.req_params = data.get('req_params', False)

    def __repr__(self):
        return '<Plugin.{}>'.format(self.name)

    @asyncio.coroutine
    def callback(self, bot, msg, data):
        pass

    @asyncio.coroutine
    def on_ready(self, bot):
        pass

    @asyncio.coroutine
    def on_message(self, bot, msg):
        pass
