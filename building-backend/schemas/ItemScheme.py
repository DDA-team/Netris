import datetime
from typing import Any
from uuid import UUID, uuid4
from pydantic import BaseModel


class ItemScheme(BaseModel):
    id: UUID
    title: str
    input_video: str
    output_video: str = None
    data: Any
    created_at: datetime.datetime
    preview_img: str
    duration: int
    is_complete: bool
