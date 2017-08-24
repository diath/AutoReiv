import asyncio
import json

from time import strftime, localtime
from math import floor
from string import capwords

import requests

from autoreiv import BasePlugin
from autoreiv import config

def format_time(timestamp):
    return strftime('%H:%M:%I', localtime(timestamp))

class Plugin(BasePlugin):
    def __init__(self):
        super().__init__({
            'name': 'Weather',
            'command': ['w', 'weather'],
            'req_params': True,
        })

    @asyncio.coroutine
    def callback(self, bot, msg, data):
        req = requests.get('http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID={}'.format(
            data.get('param'), config.get('tokens').get('weather')
        ))
        if req.status_code != 200:
            yield from bot.reply(msg, 'Invalid reply from the server.')
        else:
            info = json.loads(req.text)
            if info.get('message'):
                yield from bot.reply(msg, '{}'.format(info.get('message')))
            else:
                yield from bot.reply(msg, '{} ({}) {}°C ({}, Humidity: {}%, Sunrise: {}, Sunset: {})'.format(
                    info['name'], info['sys']['country'], floor(info['main']['temp']),
                    capwords(info['weather'][0]['description']), info['main']['humidity'],
                    format_time(info['sys']['sunrise']), format_time(info['sys']['sunset'])
                ))
