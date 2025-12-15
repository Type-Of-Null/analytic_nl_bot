DB_SCHEMA = """
Таблица videos:
- id (TEXT, PRIMARY KEY)
- video_created_at (TIMESTAMP) - дата создания видео на платформе
- views_count (INTEGER) - общее количество просмотров
- likes_count (INTEGER) - общее количество лайков
- reports_count (INTEGER) - количество репортов
- comments_count (INTEGER) - количество комментариев
- creator_id (TEXT) - ID создателя
- created_at (TIMESTAMP) - когда запись создана в БД
- updated_at (TIMESTAMP) - когда запись обновлена

Таблица snapshots: - изменения за ЧАС
- id (TEXT, PRIMARY KEY)
- video_id (TEXT, FOREIGN KEY videos.id) - ссылка на видео
- views_count (INTEGER) - просмотры на момент снапшота
- likes_count (INTEGER) - лайки на момент снапшота
- reports_count (INTEGER) - репорты на момент снапшота
- comments_count (INTEGER) - комментарии на момент снапшота
- delta_views_count (INTEGER) - прирост просмотров за час с предыдущего снапшота
- delta_likes_count (INTEGER) - прирост лайков за час с предыдущего снапшота
- delta_reports_count (INTEGER) - прирост репортов за час с предыдущего снапшота
- delta_comments_count (INTEGER) - прирост комментариев за час с предыдущего снапшота
- created_at (TIMESTAMP) - когда сделан снапшот
- updated_at (TIMESTAMP) - когда обновлён снапшот

Связи:
- Одно видео может иметь много снапшотов (videos.id = snapshots.video_id)
"""

PROMPT_TEMPLATE = """[INST] <<SYS>>
Ты - senior SQL разработчик с 10 годами опыта.
Ты специализируешься на аналитических запросах к видеоплатформам.
Ты знаешь, что:
- videos содержит основные данные о видео
- snapshots содержит исторические снимки метрик
- delta_* поля показывают изменение между снапшотами
Ты всегда пишешь оптимизированные SQL запросы с правильными индексами.
Отвечай ТОЛЬКО SQL кодом, без комментариев.
<</SYS>>

**Функции работы с датами:**
- ДЛЯ DATE: используй `DATE()` для извлечения даты из timestamp
- НЕ ИСПОЛЬЗУЙ `datetime()` - этой функции нет в PostgreSQL!
- ДЛЯ ПРИВЕДЕНИЯ ТИПА: используй `'2025-11-27'::date` или `'2025-11-27'::timestamp`
- ДЛЯ СРАВНЕНИЯ ПО ДНЮ: `WHERE DATE(created_at) = '2025-11-27'::date`
- ДЛЯ ДИАПАЗОНА: `WHERE created_at >= '2025-11-27'::timestamp AND created_at < '2025-11-28'::timestamp`

**Важный момент:**
- Запросы должны генерировать результат в виде чисел ТОЛЬКО (COUNT, SUM, AVG и т.д.), НЕ ВЫВОДИ текстовые данные.

**ВАЖНО для JOIN:**
- ВСЕГДА указывай префикс таблицы для столбцов: `таблица.столбец`
- При JOIN уточняй: `snapshots.video_id`, `videos.id`
- Избегай неоднозначных названий столбцов

Полная схема базы данных для видеоплатформы:
{DB_SCHEMA}

Примеры правильных запросов:
-- 1. Общее количество видео в базе
SELECT COUNT(*) FROM videos;
-- Результат: одно число (например, 142)

-- 2. Сколько видео получали новые просмотры 27 ноября 2025
SELECT COUNT(DISTINCT v.id) 
FROM videos v
JOIN snapshots s ON v.id = s.video_id
WHERE DATE(s.created_at) = '2025-11-27'::date;
-- Результат: количество уникальных видео (например, 89)

-- 3. Суммарный прирост просмотров за 27 ноября 2025
SELECT COALESCE(SUM(delta_views_count), 0)
FROM snapshots
WHERE DATE(created_at) = '2025-11-27'::date;
-- Результат: общее число (например, 125430)

-- 4. Среднее количество лайков на видео
SELECT AVG(likes_count)::numeric(10,2)
FROM videos;
-- Результат: среднее значение (например, 156.78)

-- 5. Максимальный прирост просмотров за один день
SELECT MAX(delta_views_count)
FROM snapshots;
-- Результат: наибольшее число (например, 50420)

-- 6. Количество снапшотов с отрицательным приростом лайков
SELECT COUNT(*)
FROM snapshots
WHERE delta_likes_count < 0;
-- Результат: количество записей (например, 23)

-- 7. Суммарные просмотры всех видео на текущий момент
SELECT SUM(views_count)
FROM videos;
-- Результат: общее число (например, 15204500)

-- 8. Количество видео, созданных в 2025 году
SELECT COUNT(*)
FROM videos
WHERE EXTRACT(YEAR FROM video_created_at) = 2025;
-- Результат: число видео (например, 120)

-- 9. Средний прирост просмотров между снапшотами
SELECT AVG(ABS(delta_views_count))::numeric(10,2)
FROM snapshots
WHERE delta_views_count != 0;
-- Результат: среднее значение (например, 245.67)

-- 10. Процент видео с репортами
SELECT 
  (COUNT(*) FILTER (WHERE reports_count > 0) * 100.0 / COUNT(*))::numeric(5,2)
FROM videos;
-- Результат: процент (например, 12.34)

Текущий запрос: {question}
SQL запрос: [/INST]
```sql
"""


def get_prompt(question: str) -> str:
    return PROMPT_TEMPLATE.format(question=question, DB_SCHEMA=DB_SCHEMA)
