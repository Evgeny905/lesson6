from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
rkb = ReplyKeyboardMarkup()
button_1 = KeyboardButton(text = 'Рассчитать')
button_2 = KeyboardButton(text = 'Информация')
rkb.add(button_1)
rkb.add(button_2)
rkb.resize_keyboard
ikb = InlineKeyboardMarkup()
button_3 = InlineKeyboardButton(text = 'Рассчитать норму калорий', callback_data = 'calories')
button_4 = InlineKeyboardButton(text = 'Формулы расчёта', callback_data = 'formulas')
ikb.add(button_3)
ikb.add(button_4)
api = ""
bot = Bot(token = api)
dp = Dispatcher(bot, storage=MemoryStorage())
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
@dp.message_handler(commands = ['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup = rkb)
@dp.message_handler(text = 'Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup = ikb)
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