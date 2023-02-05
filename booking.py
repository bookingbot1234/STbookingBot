from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode, ReplyKeyboardRemove
import aiogram.utils.markdown as md
import holidays
import logging
from functions import reservation_date, check_spotsleft, get_booking_by_id, remove_booking
from classes import ADD_BOOKING, RMV_BOOKING
from functions import submit_booking
from keyboard import rank_keyboard, coy_keyboard, date_keyboard, confirmation_keyboard, client_keyboard, rmv_kb

def setup(dp:Dispatcher):
    dp.register_message_handler(booking, text='Make Booking')
    dp.register_message_handler(cancel_book, commands='cancel', state=ADD_BOOKING.all_states) 
    dp.register_message_handler(booking_checkdate, state=ADD_BOOKING.ADD_DATE)
    dp.register_message_handler(booking_addname, state=ADD_BOOKING.ADD_NAME)
    dp.register_message_handler(booking_addrank, state=ADD_BOOKING.ADD_RANK)
    dp.register_message_handler(booking_addcoy, state=ADD_BOOKING.ADD_COY)
    dp.register_message_handler(booking_addcontact, state=ADD_BOOKING.ADD_CONTACT)
    dp.register_message_handler(booking_end, state=ADD_BOOKING.ADD_RESP)
    
    dp.register_message_handler(booking_remove, text='Cancel Booking')
    dp.register_message_handler(removal_confirmation, state=RMV_BOOKING.RMV_RESP)

async def booking(m:types.Message):
    await types.ChatActions.typing()
    result_date = get_booking_by_id(m.from_user.id)
    if result_date != None:
        await m.answer(f'You currently have an existing booking for {result_date}')
        await m.answer(f'If you wish to change the booking date, please cancel the existing booking.', reply_markup=rmv_kb())
    else:
        await ADD_BOOKING.ADD_DATE.set()
        await m.answer(f'Which date would you like to book?', reply_markup=date_keyboard(reservation_date()))

async def cancel_book(m:types.Message, state:FSMContext):
    await m.answer(
        '*Process Cancelled.*',
        reply_markup=client_keyboard(),
        parse_mode=types.ParseMode.MARKDOWN
    )
    await state.finish()
    
async def booking_checkdate(m:types.Message, state:FSMContext):
    await types.ChatActions.typing()
    async with state.proxy() as data:
        data['Date of Booking'] = m.text
        spot_no = check_spotsleft(m.text)
    if spot_no == 0:
        await m.answer(f'This date is fully booked. Please restart the bot and choose another date.')
        await state.finish()
    else:
        await ADD_BOOKING.ADD_NAME.set()
        await m.answer(f'There are {spot_no} slots available for this date.')
        await m.answer(f'Please enter your FULL NAME to proceed with booking.', reply_markup=ReplyKeyboardRemove())

async def booking_addname(m:types.Message, state:FSMContext):
    await types.ChatActions.typing()
    async with state.proxy() as data:
        data['Name'] = m.text
    await ADD_BOOKING.ADD_RANK.set()
    await m.answer(f'What is your rank?', reply_markup=rank_keyboard())
    
async def booking_addrank(m:types.Message, state:FSMContext):
    await types.ChatActions.typing()
    async with state.proxy() as data:
        data['Rank'] = m.text
    await ADD_BOOKING.ADD_COY.set()
    await m.answer(f'From which coy/node?', reply_markup=coy_keyboard())

async def booking_addcoy(m:types.Message, state:FSMContext):
    await types.ChatActions.typing()
    async with state.proxy() as data:
        data['Company'] = m.text
    await ADD_BOOKING.ADD_CONTACT.set()
    await m.answer(f'What is your phone number?', reply_markup=ReplyKeyboardRemove())

async def booking_addcontact(m:types.Message, state:FSMContext):
    await types.ChatActions.typing()
    async with state.proxy() as data:
        data['Contact'] = m.text
    msg_text = md.text(md.text('Name: ', md.code(data['Name'])),
                   md.text('Rank: ', md.code(data['Rank'])),
                   md.text('Company: ', md.code(data['Company'])),
                   md.text('Contact: ', md.code(data['Contact'])),
                   md.text('Date Selected: ', md.code(data['Date of Booking'])),
                   sep = '\n')
    msg_text_new = msg_text.replace("`", "")
    msg_text_new1 = msg_text_new.replace("\\", "")
    await ADD_BOOKING.ADD_RESP.set()
    await m.answer(f'{msg_text_new1}')
    await m.answer(f'Please confirm that your details are correct.', reply_markup=confirmation_keyboard())
#booking end needs work
async def booking_end(m:types.Message, state:FSMContext):
    if m.text == "✅":
        await types.ChatActions.typing()
        async with state.proxy() as data:
            try:
                user_id = m.from_user.id
                status_item = submit_booking(data['Name'], data['Rank'], data['Company'], data['Contact'], data['Date of Booking'], user_id)
                await state.finish()
                await m.reply(f'Successfully booked!', reply_markup=client_keyboard())
            except Exception as err:
                await m.reply(f'ERROR CODE: {err}😵‍💫 please contact [NAME]')
    else:
        await types.ChatActions.typing()
        current_state = await state.get_state()
        if current_state is None:
            return
        logging.info('Cancelling...%r', current_state)
        await state.finish()
        await m.reply(f'Cancelled process....', reply_markup= client_keyboard())

async def booking_remove(m:types.Message):
    await types.ChatActions.typing()
    await RMV_BOOKING.RMV_RESP.set()
    await m.answer(f'You have a booking under {m.from_user.id}')
    await m.answer(f'Do you want to cancel your existing booking?', reply_markup=confirmation_keyboard())
    
async def removal_confirmation(m:types.Message, state=FSMContext):
    await types.ChatActions.typing()
    if m.text == "✅":
        await types.ChatActions.typing()
        try:
            remove_booking(m.from_user.id)
            await state.finish()
            await m.reply(f'Successfully cancelled! Restart the bot to make a new booking.', reply_markup=client_keyboard())
        except Exception as err:
            await m.reply(f'ERROR CODE: {err}😵‍💫 please contact [NAME]')
    else:
        await types.ChatActions.typing()
        current_state = await state.get_state()
        if current_state is None:
            return
        logging.info('Cancelling...%r', current_state)
        await state.finish()
        await m.reply(f'Cancelled process....', reply_markup= client_keyboard())

