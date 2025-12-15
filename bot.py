import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

from config import TELEGRAM_TOKEN
from database.database import async_session, run_sql, is_safe_sql
from mistral_7b_model import load_model, generate_sql

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()


# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "🤖 Привет! Я бот для генерации SQL запросов.\n"
        "Просто напиши запрос на русском, например:\n"
        "• покажи топ 5 видео по лайкам\n"
        "• сколько всего просмотров у всех видео\n"
        "• покажи видео с количеством снапшотов больше 10\n"
        "• выведи общее количество видео за 2024 год\n"
        "• найди видео с отрицательной дельтой лайков\n"
    )


# Обработчик всех текстовых сообщений
@dp.message()
async def handle_query(message: Message):
    user_text = message.text.strip()

    try:
        # Генерируем SQL
        sql = generate_sql(user_text)
        if not is_safe_sql(sql):
            await message.answer("Небезопасный SQL")
            return
        else:
            async with async_session() as session:
                result = await run_sql(session, sql)
                await message.answer(f"{int(result[0][0])}", parse_mode="Markdown")

    except Exception as e:
        print(f"Ошибка: {e}")


async def main():

    print("🤖 Запуск бота...")
    # Загружаем модель при старте бота
    load_model()

    # Запускаем бота
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
