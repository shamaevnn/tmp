from sqlalchemy import Column, String, DateTime, func, text

from app.db.base import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True, server_default=text("gen_random_uuid()::varchar"))  # noqa

    title = Column(String(length=256), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
