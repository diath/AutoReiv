# -*- coding: utf-8 -*-
import asyncio
import random
import re

from autoreiv import BasePlugin

rdice = re.compile('(\d+)d(\d+)')

class Plugin(BasePlugin):
	def __init__(self):
		super().__init__()
		self.name = 'Roll'
		self.command = 'roll'
		self.reqParams = True

	@asyncio.coroutine
	def callback(self, bot, msg, data):
		if msg.content.find(',') != -1:
			choices = [choice.strip(' ') for choice in data.get('param').split(',')]
			yield from bot.reply(msg, '{}'.format(random.choice(choices)))
		elif msg.content.find('-') != -1:
			args = data.get('param').split('-')
			if len(args) == 2:
				yield from bot.reply(msg, '{}'.format(random.randint(int(args[0]), int(args[1]))))
		else:
			result = rdice.match(data.get('param'))
			if result:
				count = int(result.group(1))
				faces = int(result.group(2))

				if count > 10 or faces > 36:
					yield from bot.reply(msg, 'You can only roll up to 10 dice with up to 36 faces.')
				else:
					total = []
					for x in range(count):
						total.append(random.randint(1, faces))

					yield from bot.reply(msg, '{} ({} total)'.format(
						', '.join([str(x) for x in total]), sum(total)
					))
