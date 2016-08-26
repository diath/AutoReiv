# -*- coding: utf-8 -*-
import asyncio
import time

from autoreiv import AutoReiv

def main():
	while True:
		bot = AutoReiv()
		bot.load()

		try:
			bot.run(bot.config.get('login'), bot.config.get('password'))
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

if __name__ == '__main__':
	main()
