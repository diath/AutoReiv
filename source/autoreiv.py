# -*- coding: utf-8 -*-
import discord
import asyncio
import os
import sys

from plugin import BasePlugin

class AutoReiv(discord.Client):
	def __init__(self):
		print('* Starting up...')
		super().__init__()

		self.plugins = []
		self.config = __import__('config', globals(), locals(), '[*]').config
		self.trigger = self.config.get('trigger')

	def load(self):
		names = [name[:-3] for name in os.listdir('./plugins') if name.endswith('.py') and name != '__init__.py']
		for name in names:
			mod = __import__('plugins.{}'.format(name), globals(), locals(), ['*'])
			self.plugins.append(mod.Plugin())

		print('* Loaded {} plugins...'.format(len(self.plugins)))
		for plugin in self.plugins:
			print('\t- {}'.format(plugin.name))

	def get_commands(self):
		commands = []
		for plugin in self.plugins:
			if plugin.command is not None:
				if type(plugin.command) is str:
					commands.append(plugin.command)
				elif type(plugin.command) is list:
					commands.append('{} ({})'.format(plugin.command[0], ', '.join(plugin.command[1:])))

		return commands

	@asyncio.coroutine
	def on_ready(self):
		print('* Ready')

	@asyncio.coroutine
	def on_message(self, msg):
		print('* [#{}] {}: {}'.format(msg.channel, msg.author, msg.content))

		for plugin in self.plugins:
			data = {}
			if plugin.command is not None:
				if type(plugin.command) is str:
					cmd = '{}{}'.format(self.trigger, plugin.command)
					if plugin.reqParams:
						cmd += ' '

					if msg.content.startswith(cmd):
						data['command'] = plugin.command
						if plugin.reqParams:
							data['param'] = msg.content[len(cmd):]
							data['params'] = data.get('param').split(' ')

						yield from plugin.callback(self, msg, data)
						break
				elif type(plugin.command) is list:
					outer_break = False
					for command in plugin.command:
						cmd = '{}{}'.format(self.trigger, command)
						if plugin.reqParams:
							cmd += ' '

						if msg.content.startswith(cmd):
							data['command'] = command
							if plugin.reqParams:
								data['param'] = msg.content[len(cmd):]
								data['params'] = data.get('param').split(' ')

							yield from plugin.callback(self, msg, data)
							outer_break = True
							break

					if outer_break:
						break
				else:
					print('* Unknown plugin command type in {}'.format(plugin.name))
			elif plugin.pattern is not None:
				pass

	@asyncio.coroutine
	def joined(self, member):
		print('* {} has joined'.format(member.name))

	@asyncio.coroutine
	def say(self, channel, message):
		result = yield from self.send_message(channel, message)
		return result

	@asyncio.coroutine
	def reply(self, msg, message):
		result = yield from self.send_message(msg.channel, '<@{}> {}'.format(msg.author.id, message))
		return result
