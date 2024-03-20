from sqlalchemy import Column, String, ForeignKey, DateTime, func, text, DECIMAL
from sqlalchemy.orm import relationship


from app.db.base import Base


class Bet(Base):
    __tablename__ = "bets"

    id = Column(String, primary_key=True, server_default=text("gen_random_uuid()::varchar"))  # noqa

    amount = Column(DECIMAL(precision=2), nullable=False)
    status = Column(String(length=32), nullable=False)

    event_id = Column(String, ForeignKey("events.id"), index=True, nullable=False)
    event = relationship("Event", foreign_keys=[event_id], backref="bets")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
