############################
# Stage 1: dependencies
############################
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_DEV=1 \
    UV_TOOL_BIN_DIR=/usr/local/bin

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project

COPY . .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked


############################
# Stage 2: runtime
############################
FROM python:3.12-slim-bookworm

WORKDIR /app

# создаём non-root заранее
RUN groupadd --system nonroot \
    && useradd --system --create-home --gid nonroot nonroot

# копируем только нужное
COPY --from=builder /app /app

# минимальные переменные
ENV PATH="/app/.venv/bin:$PATH" \
    VIRTUAL_ENV="/app/.venv" \
    PYTHONPATH="/app"

USER nonroot

CMD ["python", "-m", "src.main"]
