import asyncio
import random
import re

from autoreiv import BasePlugin

RE_DICE = re.compile(r'(\d+)d(\d+)')
COUNT_MAX = 10
FACES_MAX = 36

class Plugin(BasePlugin):
    def __init__(self):
        super().__init__({
            'name': 'Roll',
            'command': 'roll',
            'req_params': True,
        })

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
            result = RE_DICE.match(data.get('param'))
            if result:
                count = int(result.group(1))
                faces = int(result.group(2))

                if count > COUNT_MAX or FACES_MAX > 36:
                    yield from bot.reply(msg, 'You can only roll up to {} dice with''up to {} faces.'.format(COUNT_MAX, FACES_MAX))
                else:
                    total = []
                    for _ in range(count):
                        total.append(random.randint(1, faces))

                    yield from bot.reply(msg, '{} ({} total)'.format(
                        ', '.join([str(x) for x in total]), sum(total)
                    ))
