import aiohttp
from http import HTTPStatus


class APIClient:
    def __init__(self, base_url: str) -> None:
        self.session = aiohttp.ClientSession(base_url=base_url)

    async def post(self, endpoint: str, json: dict) -> dict:
        async with self.session.post(endpoint, json=json) as response:
            if response.status == HTTPStatus.OK:
                return await response.json()
            return {"error": f"Request failed with status {response.status}"}
