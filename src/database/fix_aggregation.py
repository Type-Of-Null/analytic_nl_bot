import re


def fix_aggregation_query(sql: str) -> str:
    """Исправляет ошибки агрегации в SQL"""
    if "JOIN" in sql.upper() or "cte." in sql:
        # Не трогаем запросы с JOIN или CTE
        return sql

    # Если есть GROUP BY но нет группировки по категориям
    if "GROUP BY" in sql.upper() and "SUM(" in sql.upper():
        # Проверяем, группируем ли мы по ID (что обычно не нужно для одной суммы)
        lines = sql.upper().split("\n")
        for line in lines:
            if "GROUP BY" in line and ("ID" in line or "VIDEO_ID" in line):
                print("⚠️  Убираю ненужную GROUP BY для единой суммы")
                # Убираем GROUP BY и корректируем SELECT
                sql = sql.replace("GROUP BY id", "")
                sql = sql.replace("GROUP BY video_id", "")

                # Если в SELECT есть поля кроме агрегатных функций
                if re.search(r"SELECT\s+[^\(\s,]+", sql, re.IGNORECASE):
                    # Оставляем только агрегатную функцию
                    sql = re.sub(
                        r"SELECT\s+.+?\s+FROM",
                        "SELECT SUM(delta_views_count) FROM",
                        sql,
                        flags=re.IGNORECASE,
                    )

    # Убираем избыточные CTE для простых сумм
    if "WITH cte AS" in sql.upper() and sql.upper().count("SELECT") == 2:
        print("⚠️  Упрощаю избыточный CTE")
        # Простая эвристика: оставляем только внутренний запрос
        match = re.search(
            r"WHERE\s+(.+?)(?:\s+GROUP BY|\s+ORDER BY|\s*\))", sql, re.DOTALL
        )
        if match:
            where_clause = match.group(1)
            sql = f"SELECT COALESCE(SUM(delta_views_count), 0) FROM snapshots WHERE {where_clause}"

    return sql
