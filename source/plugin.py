import asyncio

class BasePlugin(object):
	def __init__(self):
		self.name = ''
		self.command = ''

	def __repr__(self):
		return '<Plugin.{}>'.format(self.name)

	@asyncio.coroutine
	def callback(self, bot, data):
		pass
