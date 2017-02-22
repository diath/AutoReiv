import asyncio
import os
import re

import discord

from autoreiv.config import config

PLUGINS_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'plugins')

class AutoReiv(discord.Client):
    def __init__(self):
        print('* Starting up...')
        super().__init__()

        self.plugins = []
        self.trigger = config.get('trigger')

    def load(self):
        for name in os.listdir(PLUGINS_PATH):
            if not os.path.isfile(os.path.join(PLUGINS_PATH, name)) or name == '__init__.py':
                continue

            mod = __import__('autoreiv.plugins.{}'.format(name[:-3]), globals(), locals(), ['*'])
            self.plugins.append(mod.Plugin())

        print('* Loaded {} plugins...'.format(len(self.plugins)))
        for plugin in self.plugins:
            if plugin.pattern is not None:
                plugin.pattern = re.compile(plugin.pattern)

            print('\t- {}'.format(plugin.name))

    def get_commands(self):
        commands = []
        for plugin in self.plugins:
            if plugin.command is not None:
                if isinstance(plugin.command, str):
                    commands.append(plugin.command)
                elif isinstance(plugin.command, list):
                    commands.append('{} ({})'.format(plugin.command[0], ', '.join(plugin.command[1:])))

        return commands

    @asyncio.coroutine
    def on_ready(self):
        for plugin in self.plugins:
            yield from plugin.on_ready(self)

        print('* Ready')

    @asyncio.coroutine
    def on_message(self, msg):
        for plugin in self.plugins:
            yield from plugin.on_message(self, msg)

        clean = msg.clean_content
        if not clean:
            return

        print('* [#{}] {}: {}'.format(msg.channel, msg.author.name, clean))

        if msg.author.id == self.user.id:
            pass

        for plugin in self.plugins:
            data = {}
            if plugin.command is not None:
                commands = plugin.command if isinstance(plugin.command, list) else [plugin.command]
                for command in commands:
                    cmd = '{}{}'.format(self.trigger, command)
                    if plugin.req_params:
                        cmd += ' '

                    if (not plugin.req_params and msg.content == cmd) or (plugin.req_params and msg.content.startswith(cmd)):
                        data['command'] = command
                        if plugin.req_params:
                            data['param'] = msg.content[len(cmd):]
                            data['params'] = data.get('param').split(' ')

                        yield from plugin.callback(self, msg, data)
                        break

            if plugin.pattern is not None:
                match = plugin.pattern.match(msg.content)
                if match:
                    data['match'] = match
                    data['groups'] = match.groups()

                    yield from plugin.callback(self, msg, data)

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
