import datetime
from typing import Optional

from pydantic import BaseModel


class ListDetails(BaseModel):
    url: str
    file_name: str
    is_directory: bool = False
    size: Optional[int] = None
    """Size in bytes"""
    last_modified: Optional[datetime.datetime] = None
