from typing import Optional

import httpx

import async_sendgrid


class AsyncClient:

    def __init__(
        self,
        api_key,
        impersonate_subuser: Optional[str] = None,
        host: str = 'https://api.sendgrid.com/v3',
        session=None,
        timeout=None,
    ):
        """
        Construct the Twilio SendGrid v3 API object.
        Note that the underlying client is being set up during initialization,
        therefore changing attributes in runtime will not affect HTTP client
        behaviour.

        :param auth: the authorization header
        :type auth: string
        :param impersonate_subuser: the subuser to impersonate. Will be passed
            by "On-Behalf-Of" header by underlying client.
            See https://sendgrid.com/docs/User_Guide/Settings/subusers.html
            for more details
        :type impersonate_subuser: string
        :param host: base URL for API calls
        :type host: string
        """

        self.host = host
        self.session = session
        self.timeout = timeout
        self.version = async_sendgrid.__version__
        self.useragent = 'async_sendgrid/{};python'.format(self.version)
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "User-Agent": self.useragent,
            "Accept": "*/*",
            "Content-Type": "application/json",
        }
        if impersonate_subuser:
            self.headers['On-Behalf-Of'] = impersonate_subuser

    async def __aenter__(self):
        await self.open()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    async def open(self):
        if self.session is None:
            self.session = httpx.AsyncClient(
                headers=self.headers,
            )

    async def close(self):
        if self.session is not None:
            await self.session.aclose()
            self.session = None

    async def send(self, message: dict):
        """
        Make a Twilio SendGrid v3 API request with the request body generated
        by the Mail object

        :param message: The Twilio SendGrid v3 API request body generated
            by the Mail object or dict
        """
        url = f"{self.host}/mail/send"
        if not isinstance(message, dict):
            message = message.get()

        await self.open()
        response = await self.session.post(url=url, json=message)
        if response.status_code == 202:
            return {}

        return await response.json()
