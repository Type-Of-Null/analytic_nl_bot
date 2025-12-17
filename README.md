# Analytic NL Bot

Telegram бот для аналитических запросов на естественном языке.

## Подготовка к запуску:

1. Скопируйте и настройте переменные окружения:

```bash
cp .env.example .env
# Отредактируйте .env, укажите TELEGRAM_TOKEN

```

2. Файл videos.json скопировать в папку /data

# Запустите проект:

docker compose up --build

# Запуск бота

docker compose up

# Загрузка тестовых данных

docker compose run --rm loader

# Подключение к БД

docker compose exec db psql -U user analytic_bot

# Логи бота

docker compose logs app -f
