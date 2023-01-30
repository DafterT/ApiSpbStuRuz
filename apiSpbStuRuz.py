""" Основная логика приложения """

# Основные библиотеки
from aiohttp import ClientSession, ClientConnectionError
import json
# Логирование
import logging
import logConfig
# Мои библиотеки
import dataClasses
import apiPaths


class ApiSpbStuRuz:
    async def __aenter__(self):
        # Инициализация логгера
        self._logger = logging.getLogger(logConfig.logger_name)
        self._logger.setLevel(logConfig.logging_level)
        self._logger.addHandler(logConfig.log_handler)
        self._logger.info('Creating a new session.')
        # Инициализация сессии
        self._session = ClientSession()
        return self

    async def __get_response_json(self, path: str) -> json:
        try:
            self._logger.debug(f'Try to get information from "{apiPaths.root}{path}"')
            # Запрос на сервер по адресу api + путь
            async with self._session.get(url=f'{apiPaths.root}{path}') as response:
                # Проверка корректности ответа
                if response.status == 200:
                    self._logger.debug(f'Correct status code from "{apiPaths.root}{path}"')
                    return await response.json()
                else:
                    self._logger.error(f'Incorrect status code from "{apiPaths.root}{path}": {response.status}')
                    return None
        except ClientConnectionError as e:
            # Ошибка клиента при запросе на сервер
            self._logger.error(f'Can\'t connect to the server: {e}')
            return None

    async def get_faculties(self) -> [dataClasses.Faculty]:
        self._logger.debug(f'Try to get faculties')
        faculties_json = await self.__get_response_json(apiPaths.faculties)
        self._logger.debug(f'Information about faculties: {faculties_json}')
        if faculties_json is None:
            self._logger.error(f'Returned faculties_json is None')
            return None
        if 'faculties' not in faculties_json:
            self._logger.error(f'Can\'t found "faculties" in json_file')
            return None
        try:
            faculties_list = [dataClasses.Faculty(**item) for item in faculties_json['faculties']]
            self._logger.debug(f'Information about faculties in list: {faculties_list}')
            return faculties_list
        except TypeError as e:
            self._logger.error(f'Can\'t convert to Faculty: {e}')
            return None

    async def __aexit__(self, *err):
        self._logger.info('End of the session.')
        # Уничтожение сессии
        await self._session.close()
        self._session = None
