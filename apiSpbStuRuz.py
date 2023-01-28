""" Основная логика приложения """
from aiohttp import ClientSession, ClientConnectionError
from aiologger.loggers.json import JsonLogger
import json

import dataClasses
from apiPaths import *


class ApiSpbStuRuz:
    async def __aenter__(self):
        self._session = ClientSession()
        self._logger = JsonLogger.with_default_handlers()
        return self

    async def get_response_json(self, path: str) -> json:
        await self._logger.info(path)
        try:
            async with self._session.get(url=f'{root}{path}') as response:
                return await response.json()
        except ClientConnectionError as e:
            await self._logger.error(e)

    async def __aexit__(self, *err):
        await self._session.close()
        self._session = None
        await self._logger.shutdown()
        self._logger = None
