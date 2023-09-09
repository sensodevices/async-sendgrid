from unittest.mock import patch, Mock
from httpx import AsyncClient
from async_sendgrid.utils import create_session


@patch("async_sendgrid.utils.AsyncClient", return_value=Mock(spec=AsyncClient))
def test_create_session(mock_async_client: Mock):
    """
    Test create_session utils.
    """
    create_session({"headers": "Hello World"})
    mock_async_client.assert_called_once_with(
        headers={"headers": "Hello World"}
    )
