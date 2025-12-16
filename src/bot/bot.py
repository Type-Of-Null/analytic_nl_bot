import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

from src.bot.core.config import TELEGRAM_TOKEN
from src.database.connection import async_session
from src.database.security import is_safe_sql, run_sql
from llm.mistral_client import load_model, generate_sql

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
            await message.answer("Сгенерирован небезопасный SQL-запрос")
            return

        # Выполняем SQL с обработкой ошибок
        async with async_session() as session:
            try:
                result = await run_sql(session, sql)
                if result and len(result) > 0 and result[0]:
                    await message.answer(f"{int(result[0][0])}", parse_mode="Markdown")
                else:
                    print("📭 Запрос выполнен, но не вернул данных")
            except Exception as db_error:
                await message.answer("Ошибка выполнения SQL-запроса")
                print(f"SQL ошибка: {db_error}")

    except Exception as e:
        print(f"Общая ошибка: {e}")


async def main():
    print("🤖 Запуск бота...")

    try:
        # Загружаем модель при старте бота
        load_model()
        print("✅ Модель загружена успешно")
    except Exception as e:
        print(f"Ошибка загрузки модели: {e}")
        return

    try:
        # Запускаем бота
        print("✅ Бот запущен и готов к работе")
        await dp.start_polling(bot)
    except Exception as e:
        print(f"Критическая ошибка бота: {e}")


if __name__ == "__main__":
    asyncio.run(main())
