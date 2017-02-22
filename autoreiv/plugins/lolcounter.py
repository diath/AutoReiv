import asyncio
import requests
from bs4 import BeautifulSoup

from autoreiv import BasePlugin

class Plugin(BasePlugin):
    def __init__(self):
        super().__init__({
            'name': 'League Counter',
            'command': 'counter',
            'req_params': True,
        })

    @asyncio.coroutine
    def callback(self, bot, msg, data):
        req = requests.get('http://www.lolcounter.com/champions/{}'.format(data.get('param')))
        if req.status_code != 200:
            yield from bot.reply(msg, 'Champion not found.')
        else:
            soup = BeautifulSoup(req.text, 'html.parser')
            n = 0
            names = []

            for block in soup.find_all('div', {'class': 'weak-block'}):
                for sub in block.find_all('div', {'class': 'champ-block'}):
                    for name in sub.find_all('div', {'class': 'name'}):
                        names.append(name.text)
                        break

                    n = n + 1
                    if n == 5:
                        break

                break

            yield from bot.reply(msg, 'Champions that counter {}: {}'.format(data.get('param'), ', '.join(names)))
