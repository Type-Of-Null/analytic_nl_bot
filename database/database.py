from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import sqlparse

from config import DATABASE_URL


engine = create_async_engine(DATABASE_URL, echo=False)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


def is_safe_sql(sql: str) -> bool:
    parsed = sqlparse.parse(sql)
    if not parsed:
        return False
    return parsed[0].get_type() == "SELECT"


async def run_sql(session: AsyncSession, sql: str):
    result = await session.execute(text(sql))
    return result.fetchall()
