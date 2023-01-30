""" Основная логика приложения """

# Основные библиотеки
from aiohttp import ClientSession, ClientConnectionError
import json
# Логирование
import logging
from logConfig import LogConfig
# Мои библиотеки
import dataClasses
import apiPaths


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
            self._logger.error(f'Can\'t convert {faculties_json} to Faculty: {e}')
            return None

    async def get_faculty_by_id(self, faculty_id: int) -> [dataClasses.Faculty]:
        self._logger.debug(f'Try to get faculty by id: {faculty_id}')
        faculty_json = await self.__get_response_json(f'{apiPaths.faculties}/{faculty_id}')
        self._logger.debug(f'Information about faculty: {faculty_json}')
        if faculty_json is None:
            self._logger.error(f'Returned faculty_json is None')
            return None
        try:
            faculty = dataClasses.Faculty(**faculty_json)
            self._logger.debug(f'Information about faculties in list: {faculty}')
            return faculty
        except TypeError as e:
            self._logger.error(f'Can\'t convert {faculty_json} to Faculty: {e}')
            return None

    async def __aexit__(self, *err):
        self._logger.info('End of the session.')
        # Уничтожение сессии
        await self._session.close()
        self._session = None
