from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from classes import MASTLIST
from keyboard import date_keyboard
from functions import display_data, reservation_date, count_total_signups
import aiogram.utils.markdown as md

def setup(dp:Dispatcher):
    dp.register_message_handler(masterlist, text= "Collate Data")
    dp.register_message_handler(masterlist_filtered, state=MASTLIST.SEARCH_FILTER)
    

async def masterlist(m:types.Message):
    await types.ChatActions.typing()
    await MASTLIST.SEARCH_FILTER.set()
    await m.answer(f'Please select the day to view collated info.', reply_markup=date_keyboard(reservation_date()))

async def masterlist_filtered(m:types.Message, state:FSMContext):
    await types.ChatActions.typing()
    async with state.proxy() as data:
        data['Date of Booking'] = m.text
        stat_ret = display_data(m.text)
        totalS = count_total_signups(m.text)
    for i in range(len(stat_ret)):
        text = md.text(stat_ret[i])
        await m.answer(text)
    await state.finish()
    
    await m.answer(f'There are {totalS} personnel participating for the specified date.')
    await m.answer(f'End of search results, please run /start to do anything else.')

