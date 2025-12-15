## Docker Compose

Быстрый запуск с помощью Docker Compose (создаёт Postgres БД и запускает бота):

1. Скопируйте `.env.example` в `.env` и задайте `TELEGRAM_TOKEN`:

```bash
cp .env.example .env
# отредактируйте .env и укажите TELEGRAM_TOKEN
```

2. Соберите и запустите сервисы:

```bash
docker compose up --build
```

Примечания:

- Сервис `app` дождётся доступности БД, выполнит `alembic upgrade head`, а затем запустит бота.
- Если вы измените модели, создайте файл миграции командой `alembic revision --autogenerate -m "описание"`; миграции будут автоматически применены при старте контейнера.

Заполнение БД начальными данными:

Чтобы заполнить БД данными из `data/videos.json` (предварительно скачав его) выполните одноразовый сервис `loader`:

```bash
docker compose run --rm loader
```

Это запустит `python load_data.py` после применения миграций.

Запуск бота:

```bash
python bot.py
```
