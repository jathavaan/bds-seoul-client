from abc import abstractmethod, ABC
from typing import TypeVar, Generic

from src.application.common import Response, Request

TRequest = TypeVar("TRequest")
TResponse = TypeVar("TResponse")


class RequestHandlerBase(Generic[TRequest, TResponse], ABC):
    @abstractmethod
    def handle(self, request: Request[TRequest]) -> Response[TResponse]:
        raise NotImplementedError("You must implement the handle method.")
