"""
This file contains the paths that will be used to send get requests to the SPbPU api.
It is taken from the repository on github: https://github.com/fleshka4/RuzSpbStuJavaApi

The address is formed as root + path, so there is no need to add root to each line.
However, the path is already formed based on the previous paths.

Date of create file: 01.28.2023
"""

# Ссылка на корень, базовый url
root = 'https://ruz.spbstu.ru/api/v1/ruz'
# Путь до листа кафедр/высших школ
faculties = '/faculties'
# Запрос к кафедрам/высшим школам по id (требуется дополнительное форматирование перед применением)
faculty_by_id = f'{faculties}/{{0}}'
# Получить группы в высшей школе по id школы
groups_by_faculty_id = f'{faculties}/{{0}}/groups'
# Получить всех учителей
teachers = '/teachers'
# Учитель по id (требует дополнительного форматирования)
teacher_by_id = f'{teachers}/{{0}}'
# Расписание учителя по id (требует дополнительного форматирования)
teachers_scheduler_by_id = f'{teachers}/{{0}}/scheduler'
# Расписание учителя по id в заданную дату (требует дополнительного форматирования)
teachers_scheduler_by_id_and_date = f'{teachers_scheduler_by_id}?date={{1}}-{{2}}-{{3}}'
# Получить список корпусов, "строений"
buildings = '/buildings'
# Получить корпус, "строение" по id
building_by_id = f'{buildings}/{{0}}'
# Получить комнаты в корпусе по id
rooms_by_building_id = f'{building_by_id}/rooms'
# Получить расписание комнаты в корпусе по id корпуса и id комнаты
rooms_scheduler_by_id_and_building_id = f'{rooms_by_building_id}/{{1}}/scheduler'
# Получить расписание комнаты в корпусе по id корпуса и id комнаты в определенную дату
rooms_scheduler_by_id_and_building_id_and_date = f'{rooms_scheduler_by_id_and_building_id}?date={{2}}-{{3}}-{{4}}'
# Получить расписание группы по её id
groups_scheduler_by_id = '/scheduler/{0}'
# Получить расписание группы по её id в определенную дату
groups_scheduler_by_id_and_date = f'{groups_scheduler_by_id}?date={{1}}-{{2}}-{{3}}'
# Базовый путь к поиску
search_root = '/search'
# Поиск группы по её имени
search_groups_by_name = f'{search_root}/groups?q={{0}}'
# Поиск учителя по его имени (по части)
search_teachers_by_name = f'{search_root}/teachers?q={{0}}'
# Поиск комнат по номеру (имени)
search_rooms_by_name = f'{search_root}/rooms?q={{0}}'
