import asyncio

from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.utils.exceptions import BotBlocked
from aiogram.utils.exceptions import BadRequest

from loader import db
from loader import bot
from markups import keyboards
from states.admin.main_menu import AdminMain
from states.admin.distribution import Distribution


async def distribution(message: types.Message, state: FSMContext):
    await message.answer("Что отправляем?", reply_markup=keyboards.cancel())
    await Distribution.message.set()


async def distribution_message(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['message_id'] = message.message_id

    await message.answer("Добавить кнопку?",
                         reply_markup=keyboards.check_yes_no())
    await Distribution.next()


async def distribution_keyboard(message: types.Message, state: FSMContext):
    if message.text == keyboards.text_button_yes:
        await message.answer("Название кнопки?")
        await Distribution.button_name.set()

    else:
        async with state.proxy() as data:
            await bot.copy_message(message.from_user.id, message.chat.id,
                                   data['message_id'])
            await bot.send_message(message.from_user.id, "Отправляем?",
                                   reply_to_message_id=data['message_id'],
                                   reply_markup=keyboards.check_yes_no())
        await Distribution.check.set()


async def distribution_button_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['button_text'] = message.text

    await message.reply('Ссылка?')
    await Distribution.next()


async def distribution_button_url(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['button_url'] = message.text

            await bot.copy_message(message.from_user.id, message.chat.id,
                                   data['message_id'],
                                   reply_markup=keyboards.custom_url_markup(
                                       data['button_text'], data['button_url'])
                                   )
            await bot.send_message(message.from_user.id, "Отправляем?",
                                   reply_to_message_id=data['message_id'],
                                   reply_markup=keyboards.check_yes_no())
        await Distribution.next()

    except BadRequest:
        await message.reply("Это не ссылка")


async def distribution_check(message: types.Message, state: FSMContext):
    if message.text == keyboards.text_button_yes:
        await AdminMain.main_menu.set()
        await message.answer('Рассылка началась',
                             reply_markup=keyboards.admin_menu())

        suc_send = 0
        fail_send = 0

        async with state.proxy() as data:
            for tg_id in db.get_all_tg_id():
                try:
                    if data['button_text'] != '':
                        await bot.copy_message(tg_id,
                                               message.from_user.id,
                                               data['message_id'],
                                               reply_markup=keyboards.custom_url_markup(
                                                    data['button_text'],
                                                    data['button_url']))
                    else:
                        await bot.copy_message(tg_id,
                                               message.from_user.id,
                                               data['message_id'])

                    print(f'Suc {tg_id}')
                    suc_send += 1
                    await asyncio.sleep(1)

                except BotBlocked as e:
                    fail_send += 1
                    print(f'Err {tg_id} {e}')

                except:
                    fail_send += 1
                    print(f'Err {tg_id}')

            data['button_text'] = ''
            data['button_url'] = ''
            print(f"suc_send = {suc_send}\nfail_send = {fail_send}")

    else:
        await message.answer('Отменил', reply_markup=keyboards.admin_menu())
        await AdminMain.main_menu.set()

        data['button_text'] = ''
        data['button_url'] = ''


async def distribution_send(message: types.Message, state: FSMContext):
    await message.answer(message.text)


def register_distribution(dp: Dispatcher):
    dp.register_message_handler(distribution,
                                Text(keyboards.text_button_distribution),
                                state=AdminMain)

    dp.register_message_handler(distribution_message,
                                content_types=['text', 'photo', 'video',
                                               'animation'],
                                state=Distribution.message)

    dp.register_message_handler(distribution_keyboard,
                                Text([keyboards.text_button_yes,
                                     keyboards.text_button_no]),
                                state=Distribution.keyboard)

    dp.register_message_handler(distribution_button_name,
                                content_types='text',
                                state=Distribution.button_name)

    dp.register_message_handler(distribution_button_url,
                                content_types='text',
                                state=Distribution.button_url)

    dp.register_message_handler(distribution_check,
                                Text([keyboards.text_button_yes,
                                     keyboards.text_button_no]),
                                state=Distribution.check)
