from abc import ABC, abstractmethod
from server.connections.api import ApiSession, Session
from server.connections.responses import Response, HttpResponseError


class Request(ABC):
    """The abstraction of a specific API request."""

    @abstractmethod
    def response(self) -> Response:
        pass


class Get(Request):
    """Represent a GET request."""

    def __init__(self, url: str) -> None:
        self._session: Session = ApiSession(url)

    def response(self) -> Response:
        return self._session.get()


class SafeGet(Request):
    """Represent a safe GET request.
    Raise an error if `200` response status code is not presented.
    """

    def __init__(self, url: str, status_code: int = 200) -> None:
        self._req: Request = Get(url)
        self._code: int = status_code

    def response(self) -> Response:
        if self._req.response().status_code() != self._code:
            raise HttpResponseError(
                'HTTP response error with {} status code!!!'.format(self._req.response().status_code()))
        return self._req.response()