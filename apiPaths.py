# Ссылка на корень, базовый url
root = 'https://ruz.spbstu.ru/api/v1/ruz'
# Путь до листа кафедр/высших школ
faculties = '/faculties'
# Запрос к кафедрам/высшим школам по id (требуется дополнительное форматирование перед применением)
faculties_with_id = f'{faculties}/{{0}}'
# Получить группы в высшей школе по id школы
groups_by_faculty_id = f'{faculties}/{{0}}/groups'
# Получить всех учителей
teachers = '/teachers'
