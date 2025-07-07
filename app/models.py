from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class Counter(SQLModel, table=True):
    """Counter model to persist counter state in the database"""

    __tablename__ = "counters"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, unique=True)
    value: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class CounterCreate(SQLModel, table=False):
    """Schema for creating a new counter"""

    name: str = Field(max_length=100)
    value: int = Field(default=0)


class CounterUpdate(SQLModel, table=False):
    """Schema for updating counter values"""

    value: Optional[int] = Field(default=None)


class CounterResponse(SQLModel, table=False):
    """Schema for counter API responses"""

    id: int
    name: str
    value: int
    created_at: str
    updated_at: str
