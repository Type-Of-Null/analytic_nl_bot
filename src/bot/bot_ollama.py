import asyncio
import requests
import json
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

# Ваши существующие импорты
from src.core.config import TELEGRAM_TOKEN
from src.database.connection import async_session
from src.database.security import is_safe_sql, run_sql
from llm.prompt_manager import DB_SCHEMA, PROMPT_TEMPLATE

# --- Настройки Ollama ---
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_TRANSLATOR = "phi3"
MODEL_SQL_GENERATOR = "llama3"

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()


def call_ollama_api(model_name, prompt_text):
    payload = {"model": model_name, "prompt": prompt_text, "stream": False}
    response = requests.post(OLLAMA_API_URL, data=json.dumps(payload))
    response.raise_for_status()
    result = json.loads(response.text)
    return result["response"].strip()


def translate_to_english(russian_question):
    """Переводит русский вопрос в краткую английскую фразу."""
    prompt = f"""
    Translate the following Russian question into a concise English phrase. 
    Only provide the translation, nothing else.

    Russian: '{russian_question}'

    English:
    """
    return call_ollama_api(MODEL_TRANSLATOR, prompt)


def generate_sql_with_ollama(english_question):
    """Генерирует SQL из английского вопроса с использованием схемы."""

    database_schema = DB_SCHEMA

    prompt = f"""
    {PROMPT_TEMPLATE}

    Schema:
    {database_schema}

    Question:
    {english_question}

    """
    return call_ollama_api(MODEL_SQL_GENERATOR, prompt)


def format_sql(sql: str) -> str:
    if sql.startswith("```sql"):
        sql = sql[6:].strip()
    elif sql.startswith("```"):
        sql = sql[3:].strip()

    if sql.endswith("```"):
        sql = sql[:-3].strip()
        return sql


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

        print(f"\n🧠 Запрос от пользователя: {user_text}")
        # english_query = translate_to_english(user_text)
        # sql = generate_sql_with_ollama(english_query)
        sql = format_sql(generate_sql_with_ollama(user_text))
        # print(f"🌍 Переведено: {english_query}")
        print(f"💻 Сгенерирован SQL: {sql}")

        if not is_safe_sql(sql):
            await message.answer("Сгенерирован небезопасный SQL-запрос")
            return

        # Выполняем SQL с обработкой ошибок
        async with async_session() as session:
            try:
                result = await run_sql(session, sql)
                if result and len(result) > 0 and result[0]:
                    await message.answer(f"{int(result[0][0])}", parse_mode="Markdown")
                    print(f"Результат: {int(result[0][0])}")
                else:
                    await message.answer("Нет данных")
                    print("📭 Запрос выполнен, но не вернул данных")
            except Exception as db_error:
                await message.answer("Ошибка выполнения SQL-запроса в базе данных.")
                print(f"SQL ошибка: {db_error}")

    except requests.exceptions.RequestException as e:
        await message.answer(
            "Ошибка подключения к Ollama API. Убедитесь, что Ollama запущен."
        )
        print(f"Ошибка Ollama: {e}")
    except Exception as e:
        await message.answer("Произошла непредвиденная ошибка при обработке запроса.")
        print(f"Общая ошибка: {e}")


async def main():
    print("🤖 Запуск бота...")
    print("✅ Сервис Ollama предполагается запущенным.")

    try:
        print("✅ Бот запущен и готов к работе")
        await dp.start_polling(bot)
    except Exception as e:
        print(f"Критическая ошибка бота: {e}")


if __name__ == "__main__":
    asyncio.run(main())
