import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message

from config import TELEGRAM_TOKEN

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()


@dp.message()
async def handle_query(message: Message):
    sql = generate_sql(message.text)

    await message.answer(sql)


async def main():
    load_model()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
