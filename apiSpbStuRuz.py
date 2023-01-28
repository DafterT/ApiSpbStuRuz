""" Основная логика приложения """
# Основные библиотеки
from aiohttp import ClientSession, ClientConnectionError
import json
# Логирование
import logging
from config import LogConfig
# Мои библиотеки
import dataClasses
from apiPaths import *


class ApiSpbStuRuz:
    async def __aenter__(self):
        # Инициализация логгера
        self._logger = logging.getLogger(LogConfig.logger_name)
        self._logger.setLevel(LogConfig.logging_level)
        self._logger.addHandler(LogConfig.log_handler)
        self._logger.info('Creating a new session.')
        # Инициализация сессии
        self._session = ClientSession()
        return self

    async def get_response_json(self, path: str) -> json:
        try:
            self._logger.debug(f"Try to get information from {root}{path}.")
            # Запрос на сервер по адресу api + путь
            async with self._session.get(url=f'{root}{path}') as response:
                # TODO Сделать проверку кода ответа
                return await response.json()
        except ClientConnectionError as e:
            # Ошибка клиента при запросе на сервер
            self._logger.exception(f"Can\'t connect to the server: {e}")
            return None

    async def __aexit__(self, *err):
        self._logger.info('End of the session.')
        # Уничтожение сессии
        await self._session.close()
        self._session = None
