from typing_extensions import Annotated, Literal, TypeAlias
from pydantic import BaseModel

from src.utils.transform import PropertyInfo


class ResponseInputTextParams(BaseModel):
    text: str
    """The text input"""
    type: Literal["text"]
    """The type of the input content. Always set to `text`."""


ResponseInputContentParams: TypeAlias = Annotated[
    ResponseInputTextParams,
    PropertyInfo(discriminator="type"),
]


class ResponseInputMessageParams(BaseModel):
    content: list[ResponseInputContentParams]
    """
    A list of one or many input items , containing different content
    types.
    """
    type: Literal["message"]
    """The type of the input content. Always set to `message`."""


ResponseInputItemParams: TypeAlias = Annotated[
    ResponseInputMessageParams,
    PropertyInfo(discriminator="type"),
]


class ResponseCreateParams(BaseModel):
    input: list[ResponseInputItemParams] | None = None
    """
    Optional list of input items to send to the conversation
    """
