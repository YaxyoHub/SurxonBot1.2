from aiogram.fsm.state import State, StatesGroup

class OrderState(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()
    lat = State()
    lon = State()

class AdsState(StatesGroup):
    add = State()

class AddFlowerState(StatesGroup):
    name = State()
    price = State()
    description = State()
    photos = State()

class AddToyState(StatesGroup):
    name = State()
    price = State()
    description = State()
    photos = State()

class DeleteFlowerState(StatesGroup):
    page = State()

class DeleteToyState(StatesGroup):
    page = State()

class Admin(StatesGroup):
    admin_name = State()
    admin_username = State()
    admin_id = State()

class DELETEadmin(StatesGroup):
    admin_id =State()

class ContactForm(StatesGroup):
    name = State()
    phone = State()