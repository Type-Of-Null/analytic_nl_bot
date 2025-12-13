import json
import asyncio
import subprocess
from datetime import datetime
import time
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from models import Video, Snapshot
from config import DATABASE_URL


if not DATABASE_URL:
    raise ValueError("DATABASE_URL не установлена в переменных окружения.")


async def load_data():

    subprocess.run(["alembic", "upgrade", "head"], check=True)

    engine = create_async_engine(DATABASE_URL, echo=False)

    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    with open("data/videos.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    async with async_session() as session:
        videos_count = 0
        snapshots_count = 0

        start = time.perf_counter()
        for video_data in data["videos"]:
            result = await session.execute(
                select(Video).where(Video.id == video_data["id"])
            )
            existing_video = result.scalars().first()

            if existing_video:
                continue

            video = Video(
                id=video_data["id"],
                video_created_at=datetime.fromisoformat(
                    video_data["video_created_at"].replace("Z", "+00:00")
                ).replace(tzinfo=None),
                views_count=video_data["views_count"],
                likes_count=video_data["likes_count"],
                reports_count=video_data["reports_count"],
                comments_count=video_data["comments_count"],
                creator_id=video_data["creator_id"],
                created_at=datetime.fromisoformat(
                    video_data["created_at"].replace("Z", "+00:00")
                ),
                updated_at=datetime.fromisoformat(
                    video_data["updated_at"].replace("Z", "+00:00")
                ),
            )

            for snapshot_data in video_data.get("snapshots", []):
                snapshot = Snapshot(
                    id=snapshot_data["id"],
                    video_id=snapshot_data["video_id"],
                    views_count=snapshot_data["views_count"],
                    likes_count=snapshot_data["likes_count"],
                    reports_count=snapshot_data["reports_count"],
                    comments_count=snapshot_data["comments_count"],
                    delta_views_count=snapshot_data["delta_views_count"],
                    delta_likes_count=snapshot_data["delta_likes_count"],
                    delta_reports_count=snapshot_data["delta_reports_count"],
                    delta_comments_count=snapshot_data["delta_comments_count"],
                    created_at=datetime.fromisoformat(
                        snapshot_data["created_at"].replace("Z", "+00:00")
                    ).replace(tzinfo=None),
                    updated_at=datetime.fromisoformat(
                        snapshot_data["updated_at"].replace("Z", "+00:00")
                    ).replace(tzinfo=None),
                )
                video.snapshots.append(snapshot)
                snapshots_count += 1

            session.add(video)
            videos_count += 1
        end = time.perf_counter()
        total_time = end - start
        print(f"Время выполнения: {total_time:.2f} сек")
        await session.commit()

        print(f"Данные скопированы в базу данных: {session.bind.url.database}")

    await engine.dispose()


#
if __name__ == "__main__":
    asyncio.run(load_data())
