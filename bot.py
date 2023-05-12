# -*- coding: utf-8 -*-
import logging
import os
import json
from datetime import datetime

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage


MESSAGES: dict[str, str] = json.load(open("messages.json", encoding="utf8"))
API_TOKEN = os.environ.get("BOT_TOKEN")
# API_TOKEN = ""

if not API_TOKEN:
    raise ValueError("Не указан токен в переменных окружения")

logging.basicConfig(level=logging.INFO) # , filename=f"./logs/log-{datetime.utcnow():%Y-%m-%d_%H-%M-%S}.txt")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


from handlers import *


from handlers import logic

logic.get_link_to_appointment()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
