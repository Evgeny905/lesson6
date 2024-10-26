from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from crud_functions import *
rkb = ReplyKeyboardMarkup()
button = KeyboardButton(text = 'Регистрация')
button_1 = KeyboardButton(text = 'Рассчитать')
button_2 = KeyboardButton(text = 'Информация')
button_3 = KeyboardButton(text = 'Купить')
rkb.add(button)
rkb.add(button_1)
rkb.add(button_2)
rkb.add(button_3)
rkb.resize_keyboard
ikb = InlineKeyboardMarkup()
button_4 = InlineKeyboardButton(text = get_name_products()[0], callback_data = 'product_buying')
button_5 = InlineKeyboardButton(text = get_name_products()[1], callback_data = 'product_buying')
button_6 = InlineKeyboardButton(text = get_name_products()[2], callback_data = 'product_buying')
button_7 = InlineKeyboardButton(text = get_name_products()[3], callback_data = 'product_buying')
ikb.add(button_4)
ikb.add(button_5)
ikb.add(button_6)
ikb.add(button_7)
ikb_2 = InlineKeyboardMarkup()
button_8 = InlineKeyboardButton(text = 'Рассчитать норму калорий', callback_data = 'calories')
button_9 = InlineKeyboardButton(text = 'Формулы расчёта', callback_data = 'formulas')
ikb_2.add(button_8)
ikb_2.add(button_9)
api = ""
bot = Bot(token = api)
dp = Dispatcher(bot, storage=MemoryStorage())
class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = 1000
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
@dp.message_handler(text = 'Регистрация')
async def sing_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()
@dp.message_handler(state = RegistrationState.username)
async def set_username(message, state):
    if is_included(message.text) == False:
        await state.update_data(username_ = message.text)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()
    else:
        await message.answer("Пользователь существует, введите другое имя")
        await RegistrationState.username.set()
@dp.message_handler(state = RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email_=message.text)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()
@dp.message_handler(state = RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age_=message.text)
    data = await state.get_data()
    add_user(data['username_'], data['email_'], data['age_'])
    await message.answer("Регистрация прошла успешно")
    await state.finish()
@dp.message_handler(commands = ['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup = rkb)
@dp.message_handler(text = 'Купить')
async def get_buying_list(message):
    for i in range(1, 5):
        with open(f'files/{i}.jpg', 'rb') as img:
            await message.answer_photo(img, get_all_products()[i-1])
    await message.answer('Выберите продукт для покупки:', reply_markup = ikb)
@dp.callback_query_handler(text = 'product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()
@dp.message_handler(text = 'Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup = ikb_2)
@dp.callback_query_handler(text = 'formulas')
async def get_formulas(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()
@dp.callback_query_handler(text = 'calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
    await UserState.age.set()
@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age_ = message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()
@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth_ = message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()
@dp.message_handler(state = UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight_ = message.text)
    data = await state.get_data()
    calorie_norms = 10 * int(data['weight_']) + 6,25 * int(data['growth_']) + 5 * int(data['age_']) + 5
    await message.answer(f'Ваша нора калорий {calorie_norms}')
    await state.finish()
@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)