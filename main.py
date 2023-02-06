import logging
from loguru import logger
from aiohttp import web
from aiogram.utils import executor
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import BOT_TOKEN, BASEROW_TOKEN, WEBHOOK, WEBHOOK_PATH, WEBHOOK_URL
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

async def on_startup_webhook(_):
    await bot.set_webhook(WEBHOOK_URL)
    
if __name__ == '__main__':
    start.setup(dp)
    booking.setup(dp)
    adminpage.setup(dp)
    # runner.start_polling()
    if WEBHOOK:
        logger.info("Running in Webhook Mode")
        app = web.Application()
        runner.on_startup(on_startup_webhook, webhook = True, polling = False)
        runner.set_webhook(
            webhook_path=f"/{WEBHOOK_PATH}",
            web_app = app
        )
        runner.run_app(
            host="0.0.0.0",
            port=5000
        )
    else:
        logger.info("Running in Polling Mode")
        runner.start_poling()
