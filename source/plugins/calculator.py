# -*- coding: utf-8 -*-
import asyncio
import wolframalpha

from autoreiv import BasePlugin

class Plugin(BasePlugin):
	def __init__(self):
		super().__init__()
		self.name = 'Calculator'
		self.command = 'calc'
		self.reqParams = True
		self.client = None

	@asyncio.coroutine
	def callback(self, bot, msg, data):
		if self.client is None:
			client = wolframalpha.Client(bot.config.get('tokens').get('wolfram'))

		try:
			res = client.query(data.get('param'))
		except:
			yield from bot.reply(msg, 'Invalid reply from the server.')
		finally:
			if len(res.pods) == 0:
				yield from bot.reply(msg, 'No results found.')
			else:
				result = list(res.results)
				if len(result) != 0:
					result = result[0]
				else:
					if len(res.pods) > 1:
						result = res.pods[1]
					else:
						result = {'text': 'Unknown result'}

				yield from bot.reply(msg, '{}'.format(result.text))
