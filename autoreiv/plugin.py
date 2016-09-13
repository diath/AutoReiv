import asyncio

class BasePlugin(object):
	def __init__(self):
		self.name = ''

	def __repr__(self):
		return '<Plugin.{}>'.format(self.name)

	@asyncio.coroutine
	def callback(self, bot, data):
		pass

	@asyncio.coroutine
	def on_ready(self, bot):
		pass

	@asyncio.coroutine
	def on_message(self, bot, msg):
		pass
