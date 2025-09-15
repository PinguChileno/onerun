from typing import TYPE_CHECKING, Any, Type, TypeVar, Union

from pydantic import BaseModel


if TYPE_CHECKING:
    NoneType: Type[None]
else:
    NoneType = type(None)

ResponseT = TypeVar(
    "ResponseT",
    bound=Union[
        None,
        str,
        list[Any],
        dict[str, Any],
        object,
        BaseModel,
    ]
)
