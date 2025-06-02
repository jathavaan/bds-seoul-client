from dataclasses import dataclass
from typing import TypeVar, Generic

TResponse = TypeVar("TResponse")


@dataclass
class Response(Generic[TResponse]):
    result: TResponse

    def to_dict(self) -> dict:
        return {"result": self.result}
