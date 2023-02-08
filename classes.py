from aiogram.dispatcher.filters.state import State, StatesGroup
#classes

class ADD_BOOKING(StatesGroup):
    ADD_DATE = State()
    ADD_COUNT = State()
    ADD_NAME = State()
    ADD_RANK = State()
    ADD_HUB = State()
    ADD_COY = State()
    ADD_CONTACT = State()
    ADD_RESP = State()

class RMV_BOOKING(StatesGroup):
    RMV_RESP = State()

class MASTLIST(StatesGroup):
    SEARCH_FILTER = State()
    
