import asyncio
import sqlite3

from time import time
from datetime import datetime

from autoreiv import BasePlugin
from autoreiv import config

class Plugin(BasePlugin):
	def __init__(self):
		super().__init__()
		self.name = 'History'
		self.command = 'search'
		self.reqParams = True
		self.db = None

	def __del__(self):
		if self.db:
			self.db.close()
			self.db = None

	@asyncio.coroutine
	def callback(self, bot, msg, data):
		if self.db is None:
			yield from bot.reply(msg, 'Database error.')
			return

		query = data.get('param')
		results = self.db.execute('SELECT name, timestamp, message FROM history WHERE message LIKE ? ORDER BY timestamp ASC;', ('%{}%'.format(query),)).fetchall()
		if not results:
			yield from bot.reply(msg, 'Found no occurences of "{}".'.format(query))
			return

		yield from bot.reply(msg, 'Found {} occurence(s) of "{}":\n{}'.format(
			len(results),
			query,
			'\n'.join('{} @ {}: {}'.format(result[0], datetime.fromtimestamp(result[1]).strftime('%d %B %Y, %H:%M:%S'), result[2]) for result in results)
		))

	@asyncio.coroutine
	def on_ready(self, bot):
		if self.db is None:
			self.db = sqlite3.connect('history.db')
			self.db.execute('''CREATE TABLE IF NOT EXISTS history (
				id integer PRIMARY KEY,
				name text NOT NULL,
				timestamp integer NOT NULL,
				message text NOT NULL
			);''')

	@asyncio.coroutine
	def on_message(self, bot, msg):
		if msg.author.id == bot.user.id:
			return

		if msg.content.startswith('{}{}'.format(config.get('trigger'), self.command)):
			return

		self.db.execute('INSERT INTO history VALUES (?, ?, ?, ?);', (None, msg.author.name, int(time()), msg.clean_content))
		self.db.commit()
