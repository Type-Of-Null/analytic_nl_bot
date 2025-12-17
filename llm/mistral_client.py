import time
from llama_cpp import Llama
from llm.prompt_manager import get_prompt

# Модель как глобальная переменная
model = None


# Функция загрузки модели
def load_model():
    """Загружаем модель один раз при старте бота"""
    global model
    if model is None:
        print("🚀 Загрузка модели Mistral-7B...")
        model = Llama(
            model_path="./models/mistral-7b-instruct-v0.1.Q4_K_M.gguf",
            n_ctx=8192,
            n_threads=12,
            n_batch=512,
            n_gpu_layers=0,
            use_mlock=True,
            verbose=False,
            use_mmap=True,
        )
    return model


# Функция генерации SQL
def generate_sql(question: str) -> str:
    """Принимает вопрос на русском, возвращает SQL"""
    print(f"\n🧠 Запрос от пользователя: {question}")

    # Загружаем модель если ещё не загружена
    if model is None:
        load_model()

    # Собираем промпт с вопросом пользователя
    print("⚙️ Генерация SQL...")
    start = time.perf_counter()

    # Генерируем ответ
    response = model(
        get_prompt(question),
        max_tokens=512,
        temperature=0.01,
        top_p=0.95,
        top_k=40,
        repeat_penalty=1.1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["```", "</s>", "[/INST]", ";", "\n\n"],
        echo=False,
        seed=42,
    )

    end = time.perf_counter()
    total_time = end - start
    print(f"⏱️ Время генерации: {total_time:.2f} сек")

    sql = response["choices"][0]["text"].strip()

    if sql.startswith("```sql"):
        sql = sql[6:].strip()
    elif sql.startswith("```"):
        sql = sql[3:].strip()

    if sql.endswith("```"):
        sql = sql[:-3].strip()
    print("*" * 50)
    print(f"📝 Сгенерированный SQL:\n{sql}")
    print("*" * 50)
    return sql
