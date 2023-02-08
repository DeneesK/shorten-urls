from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UrlIn(BaseModel):
    url: str


class UrlResponse(BaseModel):
    id: UUID
    original_url: str
    created_at: datetime
    is_deleted: bool


class InfoModel(BaseModel):
    id: UUID
    url_id: UUID
    counter: int
