from typing_extensions import Annotated, Literal, TypeAlias

from pydantic import BaseModel

from .._utils import PropertyInfo


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


class ResponseOutputText(BaseModel):
    text: str
    """The text output"""
    type: Literal["text"]
    """The type of the output content. Always set to `text`."""


ResponseOutputContent: TypeAlias = Annotated[
    ResponseOutputText,
    PropertyInfo(discriminator="type"),
]


class ResponseOutputMessage(BaseModel):
    content: list[ResponseOutputContent]
    """
    A list of one or many output items, containing different content
    types.
    """
    type: Literal["message"]
    """The type of the output content. Always set to `message`."""


ResponseOutputItem: TypeAlias = Annotated[
    ResponseOutputMessage,
    PropertyInfo(discriminator="type"),
]


class Response(BaseModel):
    ended: bool
    """Whether the conversation has ended."""
    output: list[ResponseOutputItem]
    """The output content of the response."""
