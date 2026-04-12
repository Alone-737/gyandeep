from __future__ import annotations

from datetime import datetime
from math import isfinite
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Student(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id: UUID | None = None
    name: str | None = Field(default=None, min_length=1)
    grade: int | None = Field(default=None, ge=1, le=12)
    created_at: datetime | None = None

    @field_validator("name")
    @classmethod
    def _strip_name(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        if not value:
            raise ValueError("name must not be empty")
        return value


class Book(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id: UUID | None = None
    filename: str = Field(min_length=1)
    file_hash: str | None = None
    total_pages: int = Field(default=0, ge=0)
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @field_validator("filename")
    @classmethod
    def _strip_filename(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("filename must not be empty")
        return value

    @field_validator("file_hash")
    @classmethod
    def _strip_file_hash(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        return value or None


class OCRPage(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id: int | None = None
    book_id: UUID
    page_index: int = Field(ge=0)
    content: str = Field(min_length=1)
    created_at: datetime | None = None

    @field_validator("content")
    @classmethod
    def _strip_content(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("content must not be empty")
        return value


class LearningEvent(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id: UUID | None = None
    student_id: UUID | None = None
    event_type: str = Field(min_length=1)
    prompt: str | None = None
    response: str | None = None
    score: float | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime | None = None

    @field_validator("event_type")
    @classmethod
    def _strip_event_type(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("event_type must not be empty")
        return value

    @field_validator("score")
    @classmethod
    def _validate_score(cls, value: float | None) -> float | None:
        if value is None:
            return None
        if not isfinite(value):
            raise ValueError("score must be a finite number")
        return value


class TextChunk(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id: int | None = None
    source: str = Field(min_length=1)
    chunk_index: int = Field(ge=0)
    content: str = Field(min_length=1)
    embedding: list[float] | None = None
    created_at: datetime | None = None

    @field_validator("source")
    @classmethod
    def _strip_source(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("source must not be empty")
        return value

    @field_validator("content")
    @classmethod
    def _strip_chunk_content(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("content must not be empty")
        return value

    @field_validator("embedding")
    @classmethod
    def _validate_embedding(cls, value: list[float] | None) -> list[float] | None:
        if value is None:
            return None
        if len(value) != 384:
            raise ValueError("embedding must have 384 dimensions")
        for item in value:
            if not isfinite(item):
                raise ValueError("embedding values must be finite")
        return value
