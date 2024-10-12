from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio
api = ""
bot = Bot(token = api)
dp = Dispatcher(bot, storage=MemoryStorage())
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
@dp.message_handler(commands = ['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью. Введите слово "Calories"')
@dp.message_handler(text = 'Calories')
async def set_age(message):
    await message.answer('Введите свой возраст:')
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