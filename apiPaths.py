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
