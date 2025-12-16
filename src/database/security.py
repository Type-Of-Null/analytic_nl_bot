from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import sqlparse


def is_safe_sql(sql: str) -> bool:
    parsed = sqlparse.parse(sql)
    if not parsed:
        return False
    return parsed[0].get_type() == "SELECT"


async def run_sql(session: AsyncSession, sql: str):
    result = await session.execute(text(sql))
    return result.fetchall()
