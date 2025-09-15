from pydantic import BaseModel


class Pagination[T](BaseModel):
    data: list[T]
    has_more: bool
