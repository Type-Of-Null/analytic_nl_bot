# Используем Python образ с uv предустановленным
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Устанавливаем не-root пользователя
RUN groupadd --system --gid 999 nonroot \
    && useradd --system --gid 999 --uid 999 --create-home nonroot

# Устанавливаем рабочую директорию
WORKDIR /app

# Включаем компиляцию байткода
ENV UV_COMPILE_BYTECODE=1

# Копируем из кэша вместо линковки, так как это mounted volume
ENV UV_LINK_MODE=copy

# Исключаем зависимости для разработки
ENV UV_NO_DEV=1

# Убеждаемся, что установленные инструменты могут быть выполнены
ENV UV_TOOL_BIN_DIR=/usr/local/bin

# Копируем файлы зависимостей
COPY pyproject.toml uv.lock ./

# Устанавливаем зависимости с кэшированием
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project

# Копируем весь проект
COPY . .

# Устанавливаем проект
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

# Добавляем venv в PATH
ENV PATH="/app/.venv/bin:$PATH"

# Сбрасываем entrypoint
ENTRYPOINT []

# Используем не-root пользователя
USER nonroot

# Запускаем приложение по умолчанию
CMD ["uv", "run", "python", "-m", "src.main"]