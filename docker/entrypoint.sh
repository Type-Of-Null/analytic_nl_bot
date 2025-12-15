#!/bin/sh
set -e

echo "Waiting for database to be ready..."

while : ; do
    python - <<'PY'
  import asyncio, os, sys
  try:
    import asyncpg
  except Exception as e:
    print('asyncpg not available yet:', e)
    sys.exit(1)

  async def test():
    try:
      dsn = os.environ.get('DATABASE_URL') or ''
      # asyncpg doesn't accept the SQLAlchemy-style prefix 'postgresql+asyncpg://'
      if dsn.startswith('postgresql+asyncpg://'):
        dsn = dsn.replace('postgresql+asyncpg://', 'postgresql://', 1)
      conn = await asyncpg.connect(dsn)
      await conn.close()
    except Exception as e:
      print('DB not ready:', e)
      sys.exit(1)
    sys.exit(0)

  asyncio.run(test())
PY
  if [ $? -eq 0 ]; then
    break
  fi
  echo "Database not ready, sleeping 1s..."
  sleep 1
done

# Запуск Alembic 
echo "Applying Alembic migrations..."
alembic upgrade head

exec "$@"
