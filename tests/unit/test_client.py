from enum import auto
import pytest
from unittest.mock import Mock, patch
from async_sendgrid.sendgrid import SendgridAPI
from pytest_httpx import HTTPXMock
from sendgrid.helpers.mail import Mail


class TestAsyncClient:
    @pytest.fixture(autouse=True)
    def _setup(self, httpx_mock: HTTPXMock) -> None:
        secret_key = "SECRET_KEY"
        impersonate_subuser = "John Smith"
        self._httpx_mock = httpx_mock
        self._service = SendgridAPI(
            api_key=secret_key, impersonate_subuser=impersonate_subuser
        )

    @pytest.fixture(autouse=True)
    def _setup_data(self):
        self._email = Mock(spec=Mail)
        self._email.get.return_value = {}

    @pytest.fixture(autouse=True)
    def _patch_version(self):
        with patch(
            "async_sendgrid.sendgrid.async_sendgrid.__version__", "0.0.3"
        ):
            yield

    @patch("async_sendgrid.sendgrid.create_session")
    def test_constructor(self, mock_create_session) -> None:
        """
        Test constructor.
        """
        assert (
            self._service.endpoint == "https://api.sendgrid.com/v3/mail/send"
        )
        assert self._service.api_key == "SECRET_KEY"
        assert self._service.version == "0.0.3"
        assert self._service.headers == {
            "Authorization": f"Bearer SECRET_KEY",
            "User-Agent": f"async_sendgrid/0.0.3;python",
            "Accept": "*/*",
            "Content-Type": "application/json",
            "On-Behalf-Of": "John Smith",
        }

    @pytest.mark.asyncio
    async def test_send(self, httpx_mock: HTTPXMock) -> None:
        """
        Test post response.
        """

        httpx_mock.add_response(
            url="https://api.sendgrid.com/v3/mail/send",
            status_code=201,
            method="POST",
        )

        async with self._service as client:
            response = await client.send(self._email)

        assert response.status_code == 201  # type: ignore

    @pytest.mark.asyncio
    async def test_resend(self, httpx_mock: HTTPXMock) -> None:
        """
        Test post response.
        """

        httpx_mock.add_response(
            url="https://api.sendgrid.com/v3/mail/send",
            status_code=201,
            method="POST",
        )

        async with self._service as client:
            await client.send(self._email)

        async with self._service as client:
            response = await client.send(self._email)

        assert response.status_code == 201  # type: ignore
