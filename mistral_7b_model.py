import time
from llama_cpp import Llama

# 1. Подключаемся к модели
model = Llama(
    model_path="./models/mistral-7b-instruct-v0.1.Q4_K_M.gguf",
    n_ctx=16384,
    n_threads=12,
    n_batch=512,
    n_gpu_layers=0,
    use_mlock=True,
    verbose=False,
    use_mmap=True,
)

# 2. Схема БД
DB_SCHEMA = """
videos(
  id TEXT PRIMARY KEY,
  video_created_at TIMESTAMP,
  views_count INTEGER,
  likes_count INTEGER,
  reports_count INTEGER,
  comments_count INTEGER,
  creator_id TEXT,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)

snapshots(
  id TEXT PRIMARY KEY,
  video_id TEXT REFERENCES videos(id),
  views_count INTEGER,
  likes_count INTEGER,
  reports_count INTEGER,
  comments_count INTEGER,
  delta_views_count INTEGER,
  delta_likes_count INTEGER,
  delta_reports_count INTEGER,
  delta_comments_count INTEGER,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)
"""

# 3. Промпт для Mistral
prompt = f"""[INST] <<SYS>>
Ты - эксперт по SQL. Отвечай только SQL кодом без объяснений.
<</SYS>>

Схема базы данных:
{DB_SCHEMA}

Покажи видео с наибольшим количеством снапшотов
Нужен только id видео и количество снапшотов
SQL запрос: [/INST]
```sql
"""


# 4. Функция генерации SQL
def generate_sql(prompt: str) -> str:
    print("🧠 Генерация SQL...")
    start = time.perf_counter()

    response = model(
        prompt, max_tokens=256, temperature=0.1, stop=["```", "</s>"], echo=False
    )

    end = time.perf_counter()
    total_time = end - start
    print(f"Время выполнения: {total_time:.2f} сек")

    sql = response["choices"][0]["text"].strip()
    print("\n📝 Сгенерированный SQL:")
    print(sql)
    return sql
