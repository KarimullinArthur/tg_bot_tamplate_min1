from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram import types
from aiogram.dispatcher.filters import Text

from loader import db
from markups import keyboards
from markups import texts
from filters.admin import Admin
from states.admin.main_menu import AdminMain, AdditionalFuncs


async def export_db(message: types.Message, state: FSMContext):
    await message.answer(message.text)


def register_additional_funcs(dp: Dispatcher):
    dp.register_message_handler(export_db,
                                Text(keyboards.text_button_export_db),
                                state=AdditionalFuncs, is_admin=True)
