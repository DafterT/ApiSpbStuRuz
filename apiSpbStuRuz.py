"""main logic"""
from aiohttp import ClientSession
import dataClasses


class ApiSpbStuRuz:
    async def __aenter__(self):
        self._session = ClientSession()
        return self

    async def get_response(self):
        url = f'https://ruz.spbstu.ru/api/v1/ruz/faculties'

        async with self._session.get(url=url) as response:
            json_response = await response.json()
            faculties = [dataClasses.Faculties(**item) for item in json_response["faculties"]]
            print(faculties)

    async def __aexit__(self, *err):
        await self._session.close()
        self._session = None
