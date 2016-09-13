import asyncio
import time

from autoreiv.autoreiv import AutoReiv
from autoreiv.config import config
from autoreiv.plugin import BasePlugin

def main():
	while True:
		bot = AutoReiv()
		bot.load()

		try:
			bot.run(config.get('login'), config.get('password'))
		except Exception as e:
			print('* Crashed with error: {}'.format(e))
		finally:
			print('* Disconnected.')

		asyncio.set_event_loop(asyncio.new_event_loop())

		print('* Waiting 10 seconds before reconnecting (press ^C to stop)...')
		try:
			time.sleep(10)
		except KeyboardInterrupt:
			break
