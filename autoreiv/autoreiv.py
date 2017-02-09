import asyncio
import os
import sys
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
            pattern = ''
            try:
                pattern = getattr(plugin, 'pattern')
            except AttributeError:
                pass
            else:
                plugin.pattern = re.compile(pattern)

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
            hasCommand = False
            hasPattern = False

            # Check for command attribute
            try:
                getattr(plugin, 'command')
            except AttributeError:
                pass
            else:
                hasCommand = True

            # Check for pattern attribute
            try:
                getattr(plugin, 'pattern')
            except AttributeError:
                pass
            else:
                hasPattern = True

            data = {}
            if hasCommand:
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
            elif hasPattern:
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
