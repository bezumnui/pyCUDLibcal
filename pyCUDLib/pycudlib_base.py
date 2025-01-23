import aiohttp
from datetime import datetime, timedelta

from pyCUDLib.errors.status_code_exception import StatusCodeException


class PyCUDLibBase:
    BASE_URL = "https://cud.libcal.com"
    BASE_HEADERS = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Safari/605.1.15",
    }

    def __init__(self):
        self._session = aiohttp.ClientSession(PyCUDLibBase.BASE_URL, headers=PyCUDLibBase.BASE_HEADERS)

    async def close(self):
        await self._session.close()

    @staticmethod
    async def basic_verification(response: aiohttp.ClientResponse):
        if not (200 <= response.status <= 300):
            raise StatusCodeException(f"Request failed with status code {response.status}"
                            f" and message {await response.text()}")

    async def post(self, url, data=None,  *args, **kwargs):
        r = await self._session.request('POST', url, *args, data=data, **kwargs)
        await self.basic_verification(r)
        return r

    async def get(self, url, *args, **kwargs):
        r = await self._session.request('GET', url, *args, **kwargs)
        await self.basic_verification(r)
        return r

    def set_referrer(self, referrer):
        self._session.headers["referer"] = referrer

    @staticmethod
    def get_formatted_day(day: datetime):
        return day.strftime("%Y-%m-%d")
