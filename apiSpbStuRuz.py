""" Основная логика приложения """

# Основные библиотеки
import aiohttp.client_exceptions
from aiohttp import ClientSession, ClientConnectionError
import json
# Логирование
import logging
from logConfig import LogConfig
# Мои библиотеки
import dataClasses
import apiPaths


class ApiSpbStuRuz:
    def __init__(self, proxy=None, timeout=5):
        # Инициализация логгера
        self._logger = logging.getLogger(LogConfig.logger_name)
        self._logger.setLevel(LogConfig.logging_level)
        self._logger.addHandler(LogConfig.log_handler)
        # Прокси
        self._proxy = proxy
        self._timeout = timeout

    async def __aenter__(self):
        # Инициализация сессии
        self._logger.info('Creating a new session.')
        self._session = ClientSession()
        return self

    # Получение json по запросу
    async def __get_response_json(self, path: str) -> json:
        try:
            self._logger.debug(f'Try to get information from "{apiPaths.root}{path}"')
            # Запрос на сервер по адресу api + путь
            async with self._session.get(url=f'{apiPaths.root}{path}', proxy=self._proxy,
                                         timeout=self._timeout) as response:
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
        except (aiohttp.client_exceptions.InvalidURL, aiohttp.client_exceptions.ClientHttpProxyError,
                aiohttp.client_exceptions.ClientProxyConnectionError) as e:
            # Ошибка с прокси
            self._logger.error(f'Invalid proxy {self._proxy}: {e}')
            return None
        except TimeoutError as e:
            self._logger.error(f'Waiting time exceeded: {e}')
            return None

    # Получение кафедр
    async def get_faculties(self) -> [dataClasses.Faculty]:
        self._logger.debug('Try to get faculties')
        faculties_json = await self.__get_response_json(apiPaths.faculties)
        self._logger.debug(f'Information about faculties: {faculties_json}')
        if faculties_json is None:
            self._logger.error('Returned faculties_json is None')
            return None
        if 'faculties' not in faculties_json:
            self._logger.error('Can\'t found "faculties" in json_file')
            return None
        try:
            faculties_list = [dataClasses.Faculty(**item) for item in faculties_json['faculties']]
            self._logger.debug(f'Information about faculties in list: {faculties_list}')
            return faculties_list
        except TypeError as e:
            self._logger.error(f'Can\'t convert {faculties_json} to Faculty: {e}')
            return None

    # Получение кафедры по id
    async def get_faculty_by_id(self, faculty_id: int) -> dataClasses.Faculty | None:
        self._logger.debug(f'Try to get faculty by id: {faculty_id}')
        faculty_json = await self.__get_response_json(f'{apiPaths.faculties_with_id.format(faculty_id)}')
        self._logger.debug(f'Information about faculty: {faculty_json}')
        if faculty_json is None:
            self._logger.error('Returned faculty_json is None')
            return None
        try:
            faculty = dataClasses.Faculty(**faculty_json)
            self._logger.debug(f'Information about faculties in list: {faculty}')
            return faculty
        except TypeError as e:
            self._logger.error(f'Can\'t convert {faculty_json} to Faculty: {e}')
            return None

    # Получение списка групп по id кафедры
    async def get_groups_on_faculties_by_id(self, faculty_id: int) -> [dataClasses.Group]:
        self._logger.debug(f'Try to get groups by faculty id: {faculty_id}')
        groups_json = await self.__get_response_json(f'{apiPaths.groups_by_faculty_id.format(faculty_id)}')
        self._logger.debug(f'Groups on faculty with id {faculty_id}: {groups_json}')
        if groups_json is None:
            self._logger.error('Returned groups_json is None')
            return None
        if 'groups' not in groups_json:
            self._logger.error(f'Can\'t found "groups" in json_file')
            return None
        try:
            groups_list = [dataClasses.Group(**item) for item in groups_json['groups']]
            self._logger.debug(f'Groups on faculty with id {faculty_id}: {groups_list}')
            return groups_list
        except TypeError as e:
            self._logger.error(f'Can\'t convert {groups_json} to Groups: {e}')
            return None

    # Получение списка учителей
    async def get_teachers(self) -> [dataClasses.Teacher]:
        self._logger.debug('Try to get teachers')
        teachers_json = await self.__get_response_json(apiPaths.teachers)
        self._logger.debug(f'Teachers in json: {teachers_json}')
        if teachers_json is None:
            self._logger.error('Returned teachers_json is None')
            return None
        if 'teachers' not in teachers_json:
            self._logger.error('Can\'t found "teachers" in json_file')
            return None
        try:
            teacher_list = [dataClasses.Teacher(**item) for item in teachers_json['teachers']]
            self._logger.debug(f'Information about teachers list: {teacher_list}')
            return teacher_list
        except TypeError as e:
            self._logger.error(f'Can\'t convert {teachers_json} to Groups: {e}')
            return None

    async def __aexit__(self, *err):
        self._logger.info('End of the session.')
        # Уничтожение сессии
        await self._session.close()
        self._session = None
