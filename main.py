import logging
from loguru import logger
from aiohttp import web
from aiogram.utils import executor
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import BOT_TOKEN, BASEROW_TOKEN
import start
import booking   
import adminpage

tele_api = BOT_TOKEN
br_api = BASEROW_TOKEN

logging.basicConfig(level = logging.INFO)
bot = Bot(token = tele_api)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage, run_tasks_by_default=True)
runner = executor.Executor(dp)
log = logging.getLogger('broadcast') 

if __name__ == '__main__':
    start.setup(dp)
    booking.setup(dp)
    adminpage.setup(dp)
    runner.start_polling()