# Analytic NL Bot

Telegram бот для аналитических запросов на естественном языке.
Используется сервис Ollama.
Были перепробованны различные LLM, для локального железа лучше подошла llama3.
В промпте указана схема используемой БД, важные правила и "дообучение" с указанием совершенных ошибок.
Есть возможность запросов на английском языке с переводом (русский -> английский)через модель phi3
После генерации SQL -> форматирование -> проверка на безопасность (sqlparse) -> обращение к БД -> вывод результата

## Подготовка к сборке:

### 1. Скопируйте и настройте переменные окружения:

```bash
cp .env.example .env
# Отредактируйте .env, укажите TELEGRAM_TOKEN
```

### 2. Файл videos.json скопировать в папку /data

#### Сборка проекта:

```bash
docker compose up --build
```

#### Запустите сборку Ollama отдельно (чтобы скачать модель)

```bash
docker compose up ollama
```

#### В другом терминале скачайте модель

```bash
docker compose exec ollama ollama pull llama3 phi3
```

#### Запустите всё вместе

```bash
docker compose up app db
```

#### Загрузка тестовых данных (запустится автоматически)

```bash
docker compose run --rm loader
```

#### Подключение к БД

```bash
docker compose exec db psql -U user analytic_bot
```

#### Логи бота

```bash
docker compose logs app -f
```

#### Остановка

```bash
docker compose down
```
