from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Video(Base):
    __tablename__ = "videos"

    id = Column(String, primary_key=True)
    video_created_at = Column(DateTime, nullable=False)
    views_count = Column(Integer, nullable=False)
    likes_count = Column(Integer, nullable=False)
    reports_count = Column(Integer, nullable=False)
    comments_count = Column(Integer, nullable=False)
    creator_id = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(
        DateTime(timezone=True), nullable=False, default=func.now(), onupdate=func.now()
    )

    snapshots = relationship(
        "Snapshot", back_populates="video", cascade="all, delete-orphan"
    )


class Snapshot(Base):
    __tablename__ = "snapshots"

    id = Column(String, primary_key=True)

    video_id = Column(String, ForeignKey("videos.id"), nullable=False)

    views_count = Column(Integer, nullable=False)
    likes_count = Column(Integer, nullable=False)
    reports_count = Column(Integer, nullable=False)
    comments_count = Column(Integer, nullable=False)
    delta_views_count = Column(Integer, nullable=False)
    delta_likes_count = Column(Integer, nullable=False)
    delta_reports_count = Column(Integer, nullable=False)
    delta_comments_count = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )

    video = relationship("Video", back_populates="snapshots")
