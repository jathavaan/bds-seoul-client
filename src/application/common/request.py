import uuid
from dataclasses import dataclass
from typing import TypeVar, Generic

TRequest = TypeVar("TRequest")


@dataclass
class RequestBase:
    correlation_id: str = uuid.uuid4().hex


class Request(Generic[TRequest], RequestBase):
    payload: TRequest
