
import asyncio
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import os

API_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

class Form(StatesGroup):
    address = State()
    name = State()
    phone = State()
    datetime = State()

@router.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    await message.answer("Привет! Я бот для записи на обслуживание кондиционеров. Напиши 'Записаться'.")

@router.message(F.text.lower() == "записаться")
async def ask_address(message: Message, state: FSMContext):
    await message.answer("Введите адрес, где будет проводиться обслуживание:")
    await state.set_state(Form.address)

@router.message(Form.address)
async def ask_name(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer("Введите ваше имя:")
    await state.set_state(Form.name)

@router.message(Form.name)
async def ask_phone(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите номер телефона:")
    await state.set_state(Form.phone)

@router.message(Form.phone)
async def ask_datetime(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("Укажите дату и время (например, 2 мая в 14:00):")
    await state.set_state(Form.datetime)

@router.message(Form.datetime)
async def confirm(message: Message, state: FSMContext):
    await state.update_data(datetime=message.text)
    data = await state.get_data()

    text = (
        f"Новая заявка:\n"
        f"Адрес: {data['address']}\n"
        f"Имя: {data['name']}\n"
        f"Телефон: {data['phone']}\n"
        f"Дата и время: {data['datetime']}"
    )

    await message.answer("✅ Заявка принята, мы скоро свяжемся с вами!")
    await bot.send_message(chat_id=ADMIN_ID, text=text)
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
