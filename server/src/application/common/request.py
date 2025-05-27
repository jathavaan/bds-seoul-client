import uuid
from dataclasses import dataclass, field
from typing import TypeVar, Generic

TRequest = TypeVar("TRequest")


@dataclass
class Request(Generic[TRequest]):
    payload: TRequest
    correlation_id: str = field(default_factory=lambda: uuid.uuid4().hex)
