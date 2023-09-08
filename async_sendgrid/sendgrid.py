from __future__ import annotations
import os
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from async_sendgrid.utils import create_session


if TYPE_CHECKING:
    from typing import Any, Optional
    from sendgrid.helpers.mail import Mail
    import httpx


class BaseAsyncClient(ABC):
    @property
    @abstractmethod
    def api_key(self) -> str:
        """Not implemented"""

    @property
    @abstractmethod
    def endpoint(self) -> str:
        """Not implemented"""

    @property
    @abstractmethod
    def version(self) -> str:
        """Not implemented"""

    @property
    @abstractmethod
    def headers(self) -> dict[Any, Any]:
        """Not implemented"""

    @abstractmethod
    async def send(self, message: dict[Any, Any] | Mail) -> httpx.Response:
        """Not implemented"""


class AsyncClient(BaseAsyncClient):
    """
    Construct the Twilio SendGrid v3 API object.
    Note that the underlying client is being set up during initialization,
    therefore changing attributes in runtime will not affect HTTP client
    behaviour.

    :param api_key: The api key issued by Sendgrid.
    :param impersonate_subuser: the subuser to impersonate. Will be passed
        by "On-Behalf-Of" header by underlying client.
        See https://sendgrid.com/docs/User_Guide/Settings/subusers.html
        for more details.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        impersonate_subuser: Optional[str] = None,
    ):
        from . import __version__

        self._api_key = api_key or os.environ["SENDGRID_API_KEY"]
        self._endpoint = "https://api.sendgrid.com/v3/mail/send"
        self._version = __version__

        self._headers = {
            "Authorization": f"Bearer {api_key}",
            "User-Agent": f"async_sendgrid/{self._version};python",
            "Accept": "*/*",
            "Content-Type": "application/json",
        }

        if impersonate_subuser:
            self._headers["On-Behalf-Of"] = impersonate_subuser

        self._session = create_session(self._headers)

    @property
    def api_key(self) -> str:
        return self._api_key

    @property
    def endpoint(self) -> str:
        return self._endpoint

    @property
    def version(self) -> str:
        return self._version

    @property
    def headers(self) -> dict[Any, Any]:
        return self._headers

    async def send(self, message: Mail) -> httpx.Response:
        """
        Make a Twilio SendGrid v3 API request with the request body generated
        by the Mail object

        :param message: The Twilio SendGrid v3 API request body generated
            by the Mail object or dict
        """
        json_message = message.get()
        response = await self._session.post(url=self._endpoint, json=json_message)
        return response

    async def __aenter__(self):
        if self._session.is_closed:
            self._session = create_session(headers=self._headers)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self._session.aclose()
