import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart, or_f, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

BOT = Bot(token="")
dp = Dispatcher()

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="⚖️ OPT NDS"),
            KeyboardButton(text="💰 OPT Money")
        ],
        [
            KeyboardButton(text="ОТМЕНА")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Что вас интересует?"
)

ALLOWED_UPDATES = [
    'update.message',  # Сообщения
    'update.callback_query',  # Нажатие инлайн кнопок
    'update.channel_post',  # Новые посты в каналах
    'update.inline_query',  # Инлайн запросы
    'update.pre_checkout_query'  # Предварительный запрос перед оплатой
]


class NDS(StatesGroup):
    one = State()
    two = State()
    three = State()


class OPT(StatesGroup):
    one = State()
    two = State()
    three = State()
    four = State()
    five = State()


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer('Здравствуйте!\nЧто вас интерсует?', reply_markup=start_kb)


@dp.message(F.data == 'skip')
async def cancel(message: types.Message, bot: Bot, state: FSMContext):
    await state.clear()
    await bot.send_message(chat_id=message.from_user.id, text='Создание заяки отменено.\nЧто вас интерсует?')


@dp.message(StateFilter(None), F.text == "⚖️ OPT NDS")
async def opt_nds(call: types.CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(NDS.one)
    await state.update_data(name=call.from_user.username)
    k = [
        [InlineKeyboardButton(text="Нынешний квартал 2024", callback_data='quarter1' + '*Нынешний квартал 2024')],
        [InlineKeyboardButton(text="Прошедшие периоды", callback_data='quarter2' + '*Прошедшие периоды')]
    ]
    keyboard_message = InlineKeyboardMarkup(inline_keyboard=k)
    await bot.send_message(chat_id=call.from_user.id,
                           text='Здравствуйте! Для связи с менеджером ответьте на пару вопросов. '
                                'За какой период интересует оптимизация?',
                           reply_markup=keyboard_message)


@dp.callback_query(NDS.one)
async def opt_nds_1(call: types.CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(NDS.two)
    await state.update_data(info=call.data.split('*')[1])
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(chat_id=call.from_user.id,
                           text='Здравствуйте! Для связи с менеджером ответьте на пару вопросов. '
                                'За какой период интересует оптимизация?')
    k = [
        [InlineKeyboardButton(text='от 0 до 10 млн', callback_data='from_0_to_10_' + '*от 0 до 10 млн')],
        [InlineKeyboardButton(text='от 10 до 50 млн', callback_data='from_10_to_50_' + '*от 10 до 50 млн')],
        [InlineKeyboardButton(text='от 50 до 100 млн', callback_data='from_50_to_100_' + '*от 50 до 100 млн')],
        [InlineKeyboardButton(text='более 100 млн', callback_data='than_100' + '*более 100 млн')]
    ]
    keyboard_message = InlineKeyboardMarkup(inline_keyboard=k)
    await bot.send_message(chat_id=call.from_user.id,
                     text=f'Какой примерно объем закупок требуется для оптимизации?',
                     reply_markup=keyboard_message)


@dp.callback_query(NDS.two)
async def opt_nds_2(call: types.CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(NDS.two)
    await state.update_data(volume=call.data.split('*')[1])
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(chat_id=call.from_user.id,
                           text=f'Какой примерно объем закупок требуется для оптимизации?')
    data = await state.get_data()
    print(data)
    await bot.send_message(chat_id=call.from_user.id,
                           text=f'Введенные данные:\n'
                                f'Период: {data["info"]}\n'
                                f'Сумма: {data["volume"]}')
    await bot.send_message(chat_id=call.from_user.id,
                           text='Спасибо за ответы! В течение 5 минут с вами свяжется менеджер для консультации.')
    await bot.send_message(chat_id=-1002217334405,
                           text=(f'⚖️ OPT NDS\n'
                                f'Введенные данные:\n'
                                f'Период: {data["info"]}\n'
                                f'Сумма: {data["volume"]}\n'
                                f'Клиент: @{call.from_user.username}'))
    await state.clear()


@dp.message(StateFilter(None), F.text == "💰 OPT Money")
async def opt_money(call: types.CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(OPT.one)
    await state.update_data(name=call.from_user.username)
    k = [
        [InlineKeyboardButton(text="на карту", callback_data='sent' + '*на карту')],
        [InlineKeyboardButton(text="криптой", callback_data='sent' + '*криптой')],
        [InlineKeyboardButton(text="наличкой", callback_data='sent' + '*наличкой')]
    ]
    keyboard_message = InlineKeyboardMarkup(inline_keyboard=k)
    await bot.send_message(chat_id=call.from_user.id, text='Здравствуйте! '
                                                           'Для связи с менеджером ответьте на пару вопросов. '
                                                           'Как вы хотите получить оптимизированные средства?',
                           reply_markup=keyboard_message)


@dp.callback_query(OPT.one)
async def opt_money_1(call: types.CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(OPT.two)
    await state.update_data(view=call.data.split('*')[1])
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(chat_id=call.from_user.id, text='Здравствуйте! '
                                                           'Для связи с менеджером ответьте на пару вопросов. '
                                                           'Как вы хотите получить оптимизированные средства?')
    await bot.send_message(chat_id=call.from_user.id, text='Введите ИНН')


@dp.message(OPT.two)
async def opt_money_2(message: types.Message, bot: Bot, state: FSMContext):
    try:
        user_input = message.text
        if user_input == 'ОТМЕНА':
            await state.clear()
            await bot.send_message(chat_id=message.from_user.id, text='Создание заяки отменено.\nЧто вас интерсует?')
        number = int(user_input)
        if 10 <= len(user_input) <= 12:
            k = [
                [InlineKeyboardButton(text='от 0 до 10 млн', callback_data='from_0_to_10_' + '*от 0 до 10 млн')],
                [InlineKeyboardButton(text='от 10 до 50 млн', callback_data='from_10_to_50_' + '*от 10 до 50 млн')],
                [InlineKeyboardButton(text='от 50 до 100 млн', callback_data='from_50_to_100_' + '*от 50 до 100 млн')],
                [InlineKeyboardButton(text='более 100 млн', callback_data='than_100' + '*более 100 млн')]
            ]
            keyboard_message = InlineKeyboardMarkup(inline_keyboard=k)
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f'Какой объем требуется оптимизировать?',
                                   reply_markup=keyboard_message)
            await state.update_data(inn=message.text)
            await state.set_state(OPT.three)
        else:
            if message.text == 'ОТМЕНА':
                pass
            else:
                await message.answer("Ошибка пожалуйста, введите верный ИНН")
    except ValueError:
        if message.text == 'ОТМЕНА':
            pass
        else:
            await message.answer("Ошибка пожалуйста, введите верный ИНН")


@dp.callback_query(OPT.three)
async def opt_money_3(call: types.CallbackQuery, bot: Bot, state: FSMContext):
    await state.update_data(sum=call.data.split('*')[1])
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(chat_id=call.from_user.id,
                           text=f'Какой объем требуется оптимизировать?')
    await bot.send_message(chat_id=call.from_user.id, text='Введите назначение платежа')
    await state.set_state(OPT.four)


@dp.message(OPT.four)
async def opt_money_4(message: types.Message, bot:Bot, state: FSMContext):
    if message.text == 'ОТМЕНА':
        await state.clear()
        await bot.send_message(chat_id=message.from_user.id, text='Создание заяки отменено.\nЧто вас интерсует?')
    else:
        await state.update_data(desired=message.text)
        await message.answer(text='Введите товар или услугу (закрывашки)')
        await state.set_state(OPT.five)


@dp.message(OPT.five)
async def opt_money_4(message: types.Message, bot: Bot, state: FSMContext):
    if message.text == 'ОТМЕНА':
        await state.clear()
        await bot.send_message(chat_id=message.from_user.id, text='Создание заяки отменено.\nЧто вас интерсует?')
    else:
        await state.update_data(target=message.text)
        data = await state.get_data()
        print(data)
        await message.answer(text=f'Введеные данные:\nИНН: {data["inn"]}\nКак получить: {data["view"]}\n'
                                  f'Сумма: {data["sum"]}\nНазначение платежа: {data["desired"]}\n'
                                  f'Желаемый товар или уcлуга: {data["target"]}')
        await bot.send_message(chat_id=message.from_user.id,
                               text='Спасибо за ответы! В течение 5 минут с вами свяжется менеджер для консультации.')
        await bot.send_message(chat_id=-1002217334405, text=f'💰 OPT Money\nВведеные данные:\nИНН: {data["inn"]}\n'
                                                            f'Как получить: {data["view"]}\nСумма: {data["sum"]}\n'
                                                            f'Назначение платежа: {data["desired"]}\n'
                                                            f'Желаемый товар или уcлуга: {data["target"]}\n'
                                                            f'Клиент: @{message.from_user.username}')
    await state.clear()


@dp.message(F.text)
async def cancel_command(message: types.Message, bot: Bot, state: FSMContext):
    if message.text == 'ОТМЕНА':
        await state.clear()
        await bot.send_message(chat_id=message.from_user.id, text='Создание заяки отменено.\nЧто вас интерсует?')
    else:
        await message.answer("Что вас интерсует?")


async def main():
    await dp.start_polling(BOT, allowed_updates=ALLOWED_UPDATES)


if __name__ == '__main__':
    asyncio.run(main())
