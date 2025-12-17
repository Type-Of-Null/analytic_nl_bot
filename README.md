# Analytic NL Bot

Telegram бот для аналитических запросов на естественном языке.
Используется сервис Ollama.
Были перепробованны различные LLM, для локального железа лучше подошла llama3.
В промпте указана схема используемой БД, важные правила и "дообучение" с указанием совершенных ошибок.
После генерации SQL -> форматирование -> проверка на безопасность (sqlparse) -> обращение к БД -> вывод результата

## Подготовка к запуску:

### 1. Установите Ollama на ваш компьютер:

#### Linux/macOS

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

#### Windows

Скачайте установщик с https://ollama.com/download

#### Запустить сервис Ollama

```bash
ollama serve
```

#### В другом терминале скачать модель

```bash
ollama pull llama3
```

### 2. Скопируйте и настройте переменные окружения:

```bash
cp .env.example .env
# Отредактируйте .env, укажите TELEGRAM_TOKEN
```

### 3. Файл videos.json скопировать в папку /data

#### Запустите проект:

```bash
docker compose up --build
```

#### Запуск бота

```bash
docker compose up
```

#### Загрузка тестовых данных

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
