from typing_extensions import Annotated, Literal, TypeAlias
from pydantic import BaseModel

from src.utils.transform import PropertyInfo


class ResponseOutputTextDTO(BaseModel):
    text: str
    """The text output"""
    type: Literal["text"]
    """The type of the output content. Always set to `text`."""


ResponseOutputContentDTO: TypeAlias = Annotated[
    ResponseOutputTextDTO,
    PropertyInfo(discriminator="type"),
]


class ResponseOutputMessageDTO(BaseModel):
    content: list[ResponseOutputContentDTO]
    """
    A list of one or many output items, containing different content
    types.
    """
    type: Literal["message"]
    """The type of the output content. Always set to `message`."""


ResponseOutputItemDTO: TypeAlias = Annotated[
    ResponseOutputMessageDTO,
    PropertyInfo(discriminator="type"),
]


class ResponseDTO(BaseModel):
    ended: bool
    """Whether the conversation has ended."""
    output: list[ResponseOutputItemDTO]
    """The output content of the response."""
