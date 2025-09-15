from typing import Generic, TypeVar
from pydantic import BaseModel


T = TypeVar('T')


class Pagination(BaseModel, Generic[T]):
    data: list[T]
    has_more: bool
