# Bot.py

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import json
from BotToken import bot_token
import importlib
import curs, curs_usd
from datetime import datetime
from time import sleep

time_now = datetime.today()
print(f"[{str(time_now)[:19]}]: Бот успешно запущен")


class MyLongPoll(VkLongPoll):
	def listen(self):
		while True:
			try:
				for event in self.check():
					yield event
			except Exception:
				time_now = datetime.today()
				print(f"[{str(time_now)[:19]}]: Соединение восстановлено")
				sleep(5)


session = vk_api.VkApi(token = bot_token)


def get_button(text, color):
	return {
			"action": {
				"type": "text",
				"payload": "{\"button\": \"" + "1" + "\"}",
				"label": f"{text}"
			},
			"color": f"{color}"
		}


keyboard = {
	"one_time": False,
	"buttons": [
		[get_button("Кошелёк", "default"), get_button("Парамайнинг", "default"), get_button("Офиц. сайт", "default")],
		[get_button("Telegram", "default"), get_button("Paratax", "default"), get_button("Блокчейн", "default")],
		[get_button("GitHub", "default"), get_button("Структура", "default"), get_button("BitTeam", "default")],
		[get_button("Курс", "positive")]
	]
}

keyboard = json.dumps(keyboard, ensure_ascii = False).encode("utf-8")
keyboard = str(keyboard.decode("utf-8"))


def send_message(user_id, msg):
	post = {
			"user_id": user_id,
			"message": msg,
			"random_id": 0,
			"keyboard": keyboard
		}

	session.method("messages.send", post)


for event in MyLongPoll(session).listen():
	if event.type == VkEventType.MESSAGE_NEW and event.to_me:
		text = event.text
		user_id = event.user_id

		if text == "Кошелёк":
			send_message(user_id, "https://wallet.prizm.space/index.html")

		elif text == "Парамайнинг":
			send_message(user_id, "https://tool-prizm.space/")

		elif text == "Офиц. сайт":
			send_message(user_id, "https://pzm.space/")

		elif text == "Telegram":
			send_message(user_id, "https://t.me/prizmdev")

		elif text == "Paratax":
			send_message(user_id, "https://www.prizm.network/services/real-paratax")

		elif text == "Блокчейн":
			send_message(user_id, "https://prizmexplorer.com/")

		elif text == "GitHub":
			send_message(user_id, "https://github.com/prizmspace/PrizmCore")

		elif text == "Структура":
			send_message(user_id, "https://prizmbank.ru/blockchain/prizm-struktura.php")

		elif text == "BitTeam":
			send_message(user_id, "https://p2p.bit.team/ru/buy/pzm")

		elif text == "Курс":
			importlib.reload(curs)
			importlib.reload(curs_usd)
			send_message(user_id, f"Курс PRIZM по CoinMarketCap\n\nPZM/RUB: ₽{curs.pzm_curs}\nPZM/USD: ${curs_usd.pzm_curs}")

		elif text == "prizm" or text == "Prizm":
			send_message(user_id, "Бот активирован!")

		else:
			send_message(user_id, "Команда не найдена")
