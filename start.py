from aiogram import Dispatcher, types
from keyboard import admin_keyboard, client_keyboard
from functions import check_isadmin

def setup(dp:Dispatcher):
    dp.register_message_handler(start, commands='start')
    dp.register_message_handler(requestadmin, text='Request Admin Access')

async def start(m:types.Message):
    await types.ChatActions.typing()
    if check_isadmin(m.from_user.id) == True:
        await m.answer(f'Hi {m.from_user.first_name}')
        await m.answer(f'What would you like to do today?', reply_markup=admin_keyboard())
    else:
        await m.answer(f'Hi {m.from_user.first_name}', reply_markup=client_keyboard())

async def requestadmin(m:types.Message):
    await types.ChatActions.typing()
    await m.answer(f'Your Telegram ID is: {m.from_user.id}')
    await m.answer(f'Please contact PRJ with this ID to be added.', reply_markup=client_keyboard())