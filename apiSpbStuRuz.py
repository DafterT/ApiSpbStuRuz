""" Основная логика приложения """
from aiohttp import ClientSession, ClientConnectionError
import json

import logging
from config import LogConfig

import dataClasses
from apiPaths import *


class ApiSpbStuRuz:
    async def __aenter__(self):
        self._logger = logging.getLogger(LogConfig.logger_name)
        self._logger.setLevel(LogConfig.logging_level)
        self._logger.addHandler(LogConfig.log_handler)
        self._logger.info('Creating a new session.')
        self._session = ClientSession()
        return self

    async def get_response_json(self, path: str) -> json:
        try:
            self._logger.debug(f"Try to get information from {root}{path}.")
            async with self._session.get(url=f'{root}{path}') as response:
                return await response.json()
        except ClientConnectionError as e:
            self._logger.exception(f"Can\'t connect to the server: {e}")

    async def __aexit__(self, *err):
        self._logger.info('End of the session.')
        await self._session.close()
        self._session = None
