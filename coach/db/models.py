from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from datetime import datetime


class Base(DeclarativeBase):
    pass


class UserProfile(Base):
    __tablename__ = "user_profile"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    age: Mapped[int] = mapped_column(Integer)
    height_cm: Mapped[int] = mapped_column(Integer)
    weight_kg: Mapped[int] = mapped_column(Integer)
    goal: Mapped[str] = mapped_column(String(50))
    experience: Mapped[str] = mapped_column(String(50))
    days_per_week: Mapped[int] = mapped_column(Integer)


class WorkoutPlan(Base):
    __tablename__ = "workout_plan"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_profile.id"))

    plan_text: Mapped[str] = mapped_column(Text)
    feedback: Mapped[str | None] = mapped_column(String(20), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
