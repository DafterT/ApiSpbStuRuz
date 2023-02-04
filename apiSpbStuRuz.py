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

    # Функция для обработки json, путь к api, текст для логирования
    async def __get_something(self, function, api_path: str, text: str):
        self._logger.debug(f'Try to get {text}')
        response_json = await self.__get_response_json(api_path)
        self._logger.debug(f'Information about {text} in json: {response_json}')
        try:
            returned_information = function(response_json)
            self._logger.debug(f'Returned information: {returned_information}')
            return returned_information
        except TypeError as e:
            if response_json is None:
                # Ошибка при подключении
                self._logger.error('Returned json is None')
            elif 'got an unexpected keyword argument' in e.args[0]:
                # Вернувшийся json не корректен (возможно не правильный тип данных при преобразовании
                self._logger.error(f'Can\'t convert json: {e}')
            else:
                # Если вдруг что-то пошло не так, чтоб закинуть инфу в лог
                self._logger.error(f'Something goes wrong: {e}')
            return None
        except KeyError as e:
            # При поиске значения в json введен неверный ключ
            self._logger.error(f'Can\'t found key in json_file: {e}')
            return None

    # Получение кафедр
    async def get_faculties(self) -> [dataClasses.Faculty]:
        faculties_list = await self.__get_something(
            lambda faculties_json: [dataClasses.Faculty(**item) for item in faculties_json['faculties']],
            apiPaths.faculties,
            "Faculties"
        )
        return faculties_list

    # Получение кафедры по id
    async def get_faculty_by_id(self, faculty_id: int) -> dataClasses.Faculty | None:
        faculty = await self.__get_something(
            lambda faculty_json: dataClasses.Faculty(**faculty_json),
            apiPaths.faculty_by_id.format(faculty_id),
            "Faculty"
        )
        return faculty

    # Получение списка групп по id кафедры
    async def get_groups_on_faculties_by_id(self, faculty_id: int) -> [dataClasses.Group]:
        groups_list = await self.__get_something(
            lambda groups_json: [dataClasses.Group(**item) for item in groups_json['groups']],
            apiPaths.groups_by_faculty_id.format(faculty_id),
            "groups"
        )
        return groups_list

    # Получение списка учителей
    async def get_teachers(self) -> [dataClasses.Teacher]:
        teacher_list = await self.__get_something(
            lambda teachers_json: [dataClasses.Teacher(**item) for item in teachers_json['teachers']],
            apiPaths.teachers,
            "teachers"
        )
        return teacher_list

    # Выдает преподавателя по id
    async def get_teacher_by_id(self, teacher_id: int) -> dataClasses.Teacher | None:
        teacher = await self.__get_something(
            lambda teacher_json: dataClasses.Teacher(**teacher_json),
            apiPaths.teacher_by_id.format(teacher_id),
            "Teacher"
        )
        return teacher

    # Выдает расписание преподавателя по id
    async def get_teacher_scheduler_by_id(self, teacher_id: int) -> dataClasses.SchedulerTeacher | None:
        scheduler = await self.__get_something(
            lambda scheduler_json: dataClasses.SchedulerTeacher(**scheduler_json),
            apiPaths.teachers_scheduler_by_id.format(teacher_id),
            "Teachers scheduler"
        )
        return scheduler

    # Выдает расписание преподавателя по id и дате
    async def get_teacher_scheduler_by_id_and_date(self, teacher_id: int,
                                                   year: int, month: int,
                                                   day: int) -> dataClasses.SchedulerTeacher | None:
        scheduler = await self.__get_something(
            lambda scheduler_json: dataClasses.SchedulerTeacher(**scheduler_json),
            apiPaths.teachers_scheduler_by_id_and_date.format(teacher_id, year, month, day),
            "Teachers scheduler by day"
        )
        return scheduler

    # Получить список корпусов
    async def get_buildings(self) -> [dataClasses.Building]:
        buildings = await self.__get_something(
            lambda buildings_json: [dataClasses.Building(**item) for item in buildings_json['buildings']],
            apiPaths.buildings,
            "Buildings"
        )
        return buildings

    # Получить корпус по id
    async def get_building_by_id(self, building_id: int) -> dataClasses.Building:
        building = await self.__get_something(
            lambda building_json: dataClasses.Building(**building_json),
            apiPaths.building_by_id.format(building_id),
            "Building"
        )
        return building

    # Получить корпус по id
    async def get_rooms_by_building_id(self, building_id: int) -> [dataClasses.Room]:
        rooms = await self.__get_something(
            lambda rooms_json: [dataClasses.Room(**item) for item in rooms_json['rooms']],
            apiPaths.rooms_by_building_id.format(building_id),
            "Rooms"
        )
        return rooms

    async def get_rooms_scheduler_by_id_and_building_id(self,
                                                        building_id: int, room_id: int) -> dataClasses.SchedulerRoom:
        rooms_scheduler = await self.__get_something(
            lambda rooms_scheduler_json: dataClasses.SchedulerRoom(**rooms_scheduler_json),
            apiPaths.rooms_scheduler_by_id_and_building_id.format(building_id, room_id),
            "Room's scheduler"
        )
        return rooms_scheduler

    async def get_rooms_scheduler_by_id_and_building_id_and_date(self,
                                                                 building_id: int,
                                                                 room_id: int,
                                                                 year: int, month: int, day: int
                                                                 ) -> dataClasses.SchedulerRoom:
        rooms_scheduler = await self.__get_something(
            lambda rooms_scheduler_json: dataClasses.SchedulerRoom(**rooms_scheduler_json),
            apiPaths.rooms_scheduler_by_id_and_building_id_and_date.format(building_id, room_id, year, month, day),
            "Room's scheduler by date"
        )
        return rooms_scheduler

    async def get_groups_scheduler_by_id(self, group_id: int) -> dataClasses.SchedulerGroup:
        groups_scheduler = await self.__get_something(
            lambda groups_scheduler_json: dataClasses.SchedulerGroup(**groups_scheduler_json),
            apiPaths.groups_scheduler_by_id.format(group_id),
            "Group's scheduler"
        )
        return groups_scheduler

    async def get_groups_scheduler_by_id_and_date(self, group_id: int,
                                                  year: int, month: int, day: int) -> dataClasses.SchedulerGroup:
        groups_scheduler = await self.__get_something(
            lambda groups_scheduler_json: dataClasses.SchedulerGroup(**groups_scheduler_json),
            apiPaths.groups_scheduler_by_id_and_date.format(group_id, year, month, day),
            "Group's scheduler by date"
        )
        return groups_scheduler

    async def __aexit__(self, *err):
        self._logger.info('End of the session.')
        # Уничтожение сессии
        await self._session.close()
        self._session = None
