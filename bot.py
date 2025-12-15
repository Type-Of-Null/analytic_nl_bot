# bot.py - ИСПРАВЛЕННАЯ версия
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

    # Показываем что бот думает
    thinking_msg = await message.answer("🤔 Думаю над запросом...")

    try:
        # Генерируем SQL
        sql = generate_sql(user_text)

        # Удаляем сообщение "Думаю..."
        await thinking_msg.delete()

        # Отправляем сгенерированный SQL
        await message.answer(f"```sql\n{sql}\n```", parse_mode="Markdown")

        # Пока пропускаем проверку безопасности и выполнение
        # TODO: позже добавить:
        # if not is_safe_sql(sql):
        #     await message.answer("❌ Небезопасный SQL")
        #     return
        #
        # async with async_session() as session:
        #     rows = await run_sql(session, sql)
        #     if rows:
        #         text = "\n".join(str(row) for row in rows[:10])
        #         await message.answer(f"Результат:\n{text}")
        #     else:
        #         await message.answer("📭 Нет данных по запросу")

    except Exception as e:
        await message.answer(f"❌ Ошибка: {str(e)}")
        print(f"Ошибка: {e}")


async def main():
    # Загружаем модель при старте бота
    print("🤖 Запуск бота...")
    load_model()

    # Запускаем бота
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
