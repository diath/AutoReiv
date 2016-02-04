# -*- coding: utf-8 -*-
import asyncio

from autoreiv import BasePlugin

class Plugin(BasePlugin):
	def __init__(self):
		super().__init__()
		self.name = 'Commands'
		self.command = 'commands'
		self.reqParams = False

	@asyncio.coroutine
	def callback(self, bot, msg, data):
		yield from bot.reply(msg, 'Available commands (trigger "{}"): {}'.format(bot.trigger, ', '.join(bot.get_commands())))
