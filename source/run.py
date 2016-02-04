# -*- coding: utf-8 -*-
from autoreiv import AutoReiv

bot = AutoReiv()
bot.load()

try:
	bot.run(bot.config.get('login'), bot.config.get('password'))
except KeyboardInterrupt:
	bot.close()
finally:
	print('* Bye!')
