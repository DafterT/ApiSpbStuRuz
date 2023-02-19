"""
A file with the main logic of the library.
Requests are generated here, and return values are processed.

This library is completely asynchronous, which allows you to greatly speed up requests.
It is based on the aiohttp library

The library was created for educational purposes as a pet project.

Date of create file: 01.28.2023
"""

# Main logic libraries
from aiohttp import ClientSession, client_exceptions
import json
# Logging libraries
import logging
# Other libraries
from typing import Callable
from . import apiPaths
from . import dataClasses
from . import apiSpbStuRuzExeptions
from . import LogConfig


class ApiSpbStuRuz:
    """
    This class contains a set of methods that allow you to make requests to the API of the SPbPU schedule.
    All methods in this class are asynchronous.

    Must be created only using async with statements
    """

    def __init__(self, proxy=None, timeout=5):
        """
        Initialization of synchronous parameters.

        Here you can pass the proxy in the format that the aiohttp library requires,
        as well as the timeout after which the request will drop and give an error.

        :param proxy: If you want to use a proxy for requests, then pass them to this parameter.
        Proxies are not used as standard. The proxy should be transmitted in the format required by the aiohttp library
        :param timeout: If you want to change the request timeout from 5 seconds, then use this parameter
        """
        # Инициализация логгера
        self._logger = logging.getLogger(LogConfig.logger_name)
        self._logger.setLevel(LogConfig.logging_level)
        self._logger.addHandler(LogConfig.log_handler)
        # Прокси
        self._proxy = proxy
        self._timeout = timeout

    async def __aenter__(self):
        """
        Constructor for With Statement Context Manager.
        Initializes the session to create a TCP connection to the server.
        """
        # Инициализация сессии
        self._logger.info('Creating a new session.')
        self._session = ClientSession()
        return self

    # Получение json по запросу
    async def __get_response_json(self, path: str) -> json:
        """
        A private function that makes a request of the format: root from apiPaths.py + path,
        which is passed to it as a parameter. If the response is correct, it returns the json of the response.

        The function handles a number of errors with proxy, connection and responses from the server.

        :param path: The path to make the request.
        Root does not need to be specified in the path, it is added automatically when requested.
        :return: Returns a response from the server in json format.
        """
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
                    raise apiSpbStuRuzExeptions.ResponseCodeError(f'{apiPaths.root}{path}', response.status)
        except client_exceptions.ClientConnectionError as e:
            # Ошибка клиента при запросе на сервер
            self._logger.error(f'Can\'t connect to the server: {e}')
            raise apiSpbStuRuzExeptions.ClientConnectionError(e)
        except (client_exceptions.InvalidURL, client_exceptions.ClientHttpProxyError,
                client_exceptions.ClientProxyConnectionError) as e:
            # Ошибка с прокси
            self._logger.error(f'Invalid proxy {self._proxy}: {e}')
            raise apiSpbStuRuzExeptions.ProxyError(self._proxy, e)
        except TimeoutError as e:
            # Превышено время ожидания ответа
            self._logger.error(f'Waiting time exceeded: {e}')
            raise apiSpbStuRuzExeptions.TimeOutError(e)

    # Функция для обработки json, путь к api, текст для логирования
    async def __get_something(self, function: Callable, api_path: str, text: str):
        """
        A function for converting a json response to a class format from dataClasses.py.
        Handles errors when converting json to a class.

        :param function: A function for converting from a json response to the required dataclass.
        :param api_path: The path where the request will be made (root will be added automatically).
        :param text: Text for logging.
        :return:
        """
        self._logger.debug(f'Try to get {text}')
        response_json = await self.__get_response_json(api_path)
        self._logger.debug(f'Information about {text} in json: {response_json}')
        try:
            returned_information = function(response_json)
            self._logger.debug(f'Returned information: {returned_information}')
            return returned_information
        except TypeError as e:
            if 'got an unexpected keyword argument' in e.args[0]:
                # Вернувшийся json не корректен (возможно не правильный тип данных при преобразовании
                self._logger.error(f'Can\'t convert json {response_json}: {e}')
                raise apiSpbStuRuzExeptions.JsonConvertError(response_json, e)
            # Если вдруг что-то пошло не так, чтоб закинуть информацию в лог
            self._logger.error(f'Something goes wrong: {e}')
            raise apiSpbStuRuzExeptions.JsonTypeError(e)
        except KeyError as e:
            # При поиске значения в json введен неверный ключ
            self._logger.error(f'Can\'t found key in json_file: {e}')
            raise apiSpbStuRuzExeptions.JsonKeyError(e)

    # Получение кафедр
    async def get_faculties(self) -> [dataClasses.Faculty]:
        """
        Makes a request for departments/higher schools. You may need to get an id by name.

        :return: A list of departments/higher schools.
        """
        faculties_list = await self.__get_something(
            lambda faculties_json: [dataClasses.Faculty(**item) for item in faculties_json['faculties']],
            apiPaths.faculties,
            "Faculties"
        )
        return faculties_list

    # Получение кафедры по id
    async def get_faculty_by_id(self, faculty_id: int) -> dataClasses.Faculty:
        """
        Returns the department/higher school by its id.
        You may need to get the name by id.

        :param faculty_id: id of department/higher school.
        :return: Department/Higher school
        """
        faculty = await self.__get_something(
            lambda faculty_json: dataClasses.Faculty(**faculty_json),
            apiPaths.faculty_by_id.format(faculty_id),
            "Faculty"
        )
        return faculty

    # Получение списка групп по id кафедры
    async def get_groups_on_faculties_by_id(self, faculty_id: int) -> [dataClasses.Group]:
        """
        :param faculty_id: id of department/higher school.
        :return: List of groups in this department/higher school.
        """
        groups_list = await self.__get_something(
            lambda groups_json: [dataClasses.Group(**item) for item in groups_json['groups']],
            apiPaths.groups_by_faculty_id.format(faculty_id),
            "Groups"
        )
        return groups_list

    # Получение списка учителей
    async def get_teachers(self) -> [dataClasses.Teacher]:
        """
        Be careful, the request is executed for a long time because the returned file contains many positions.

        :return: List of all teachers.
        """
        teacher_list = await self.__get_something(
            lambda teachers_json: [dataClasses.Teacher(**item) for item in teachers_json['teachers']],
            apiPaths.teachers,
            "Teachers"
        )
        return teacher_list

    # Выдает преподавателя по id
    async def get_teacher_by_id(self, teacher_id: int) -> dataClasses.Teacher:
        """
        :param teacher_id: teacher id (exactly id, not oid).
        :return: Information about the teacher.
        """
        teacher = await self.__get_something(
            lambda teacher_json: dataClasses.Teacher(**teacher_json),
            apiPaths.teacher_by_id.format(teacher_id),
            "Teacher"
        )
        return teacher

    # Выдает расписание преподавателя по id
    async def get_teacher_scheduler_by_id(self, teacher_id: int) -> dataClasses.SchedulerTeacher:
        """
        :param teacher_id: teacher id (exactly id, not oid).
        :return: Information about the teacher's scheduler.
        """
        scheduler = await self.__get_something(
            lambda scheduler_json: dataClasses.SchedulerTeacher(**scheduler_json),
            apiPaths.teachers_scheduler_by_id.format(teacher_id),
            "Teachers scheduler"
        )
        return scheduler

    # Выдает расписание преподавателя по id и дате
    async def get_teacher_scheduler_by_id_and_date(self, teacher_id: int,
                                                   year: int, month: int,
                                                   day: int) -> dataClasses.SchedulerTeacher:
        """
        :param teacher_id: teacher id (exactly id, not oid).
        :param day: A day in the week, the schedule of which you need to get.
        :param month: Required month.
        :param year: Required year.
        :return: Information about the teacher's scheduler.
        """
        scheduler = await self.__get_something(
            lambda scheduler_json: dataClasses.SchedulerTeacher(**scheduler_json),
            apiPaths.teachers_scheduler_by_id_and_date.format(teacher_id, year, month, day),
            "Teachers scheduler by day"
        )
        return scheduler

    # Получить список корпусов
    async def get_buildings(self) -> [dataClasses.Building]:
        """
        Get the buildings that are in the schedule.

        Please note that the buildings are not all fully filled.
        Also, the structure can be anything where couples can pass, including remote ones.

        :return: List of buildings.
        """
        buildings = await self.__get_something(
            lambda buildings_json: [dataClasses.Building(**item) for item in buildings_json['buildings']],
            apiPaths.buildings,
            "Buildings"
        )
        return buildings

    # Получить корпус по id
    async def get_building_by_id(self, building_id: int) -> dataClasses.Building:
        """
        :param building_id: id of the building itself.
        :return: Building Information. Be careful, often the information is not filled in completely.
        """
        building = await self.__get_something(
            lambda building_json: dataClasses.Building(**building_json),
            apiPaths.building_by_id.format(building_id),
            "Building"
        )
        return building

    # Получить аудитории в здании по его id
    async def get_rooms_by_building_id(self, building_id: int) -> [dataClasses.Room]:
        """
        Get a list of classrooms that are located in the building by id.

        :param building_id: id of the building where the audience is being searched.
        :return: List of all auditories
        """
        rooms = await self.__get_something(
            lambda rooms_json: [dataClasses.Room(**item) for item in rooms_json['rooms']],
            apiPaths.rooms_by_building_id.format(building_id),
            "Rooms"
        )
        return rooms

    # Получить расписание в аудитории по id здания и аудитории
    async def get_rooms_scheduler_by_id_and_building_id(self,
                                                        building_id: int,
                                                        room_id: int
                                                        ) -> dataClasses.SchedulerRoom:
        """
        Get a schedule in a class by its id in a specific building by its id.

        :param building_id: id of the building where the audience is being searched.
        :param room_id: id of the room where you need to view the schedule.
        :return: Schedule in the classroom.
        """
        rooms_scheduler = await self.__get_something(
            lambda rooms_scheduler_json: dataClasses.SchedulerRoom(**rooms_scheduler_json),
            apiPaths.rooms_scheduler_by_id_and_building_id.format(building_id, room_id),
            "Room's scheduler"
        )
        return rooms_scheduler

    # Получить расписание в аудитории по id здания и аудитории в определенную дату
    async def get_rooms_scheduler_by_id_and_building_id_and_date(self,
                                                                 building_id: int,
                                                                 room_id: int,
                                                                 year: int, month: int, day: int
                                                                 ) -> dataClasses.SchedulerRoom:
        """
        Get a schedule in a class by its id in a specific building by its id.

        :param building_id: id of the building where the audience is being searched.
        :param room_id: id of the room where you need to view the schedule.
        :param day: A day in the week, the schedule of which you need to get.
        :param month: Required month.
        :param year: Required year.
        :return: Schedule in the classroom
        """
        rooms_scheduler = await self.__get_something(
            lambda rooms_scheduler_json: dataClasses.SchedulerRoom(**rooms_scheduler_json),
            apiPaths.rooms_scheduler_by_id_and_building_id_and_date.format(building_id, room_id, year, month, day),
            "Room's scheduler by date"
        )
        return rooms_scheduler

    # Получить расписание группы по id
    async def get_groups_scheduler_by_id(self, group_id: int) -> dataClasses.SchedulerGroup:
        """
        Get the schedule of a group by its id.

        :param group_id: id of the requested group.
        :return: Schedule of the requested group.
        """
        groups_scheduler = await self.__get_something(
            lambda groups_scheduler_json: dataClasses.SchedulerGroup(**groups_scheduler_json),
            apiPaths.groups_scheduler_by_id.format(group_id),
            "Group's scheduler"
        )
        return groups_scheduler

    # Получить расписание группы по id на определенную дату
    async def get_groups_scheduler_by_id_and_date(self, group_id: int,
                                                  year: int, month: int, day: int
                                                  ) -> dataClasses.SchedulerGroup:
        """
        Get the schedule of a group by its id.

        :param group_id: id of the requested group.
        :param day: A day in the week, the schedule of which you need to get.
        :param month: Required month.
        :param year: Required year.
        :return: Schedule of the requested group.
        """
        groups_scheduler = await self.__get_something(
            lambda groups_scheduler_json: dataClasses.SchedulerGroup(**groups_scheduler_json),
            apiPaths.groups_scheduler_by_id_and_date.format(group_id, year, month, day),
            "Group's scheduler by date"
        )
        return groups_scheduler

    # Получить группу по её имени
    async def get_groups_by_name(self, groups_name: str) -> [dataClasses.Group]:
        """
        Get a group by name. Note that the request may return a tuple of groups
        because the name value must include the requested name, and not be equal to it.

        :param groups_name: The name of group.
        :return: List of groups whose name contains the input string.
        """
        groups = await self.__get_something(
            lambda groups_json: [dataClasses.Group(**item) for item in groups_json['groups']],
            apiPaths.search_groups_by_name.format(groups_name),
            "Group's by name"
        )
        return groups

    # Получить учителя по его имени
    async def get_teachers_by_name(self, teachers_name: str) -> [dataClasses.Teacher]:
        """
        Get a teacher by name. Note that the request may return a tuple of teachers
        because the name value must include the requested name, and not be equal to it.

        :param teachers_name: The name of teacher.
        :return: List of teacher whose name contains the input string.
        """
        teachers = await self.__get_something(
            lambda teachers_json: [dataClasses.Teacher(**item) for item in teachers_json['teachers']],
            apiPaths.search_teachers_by_name.format(teachers_name),
            "Teacher's by name"
        )
        return teachers

    # Получить аудиторию по её имени
    async def get_rooms_by_name(self, rooms_name: str) -> [dataClasses.Auditory]:
        """
        Get a room by name. Note that the request may return a tuple of rooms
        because the name value must include the requested name, and not be equal to it.

        :param rooms_name: The name of rooms.
        :return: List of rooms whose name contains the input string.
        """
        rooms = await self.__get_something(
            lambda rooms_json: [dataClasses.Auditory(**item) for item in rooms_json['rooms']],
            apiPaths.search_rooms_by_name.format(rooms_name),
            "Room's by name"
        )
        return rooms

    async def __aexit__(self, *err):
        """
        Deconstructor for With Statement Context Manager.
        Closes TCP connection
        """
        self._logger.info('End of the session.')
        # Уничтожение сессии
        await self._session.close()
        self._session = None
