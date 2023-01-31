import logging
import datetime


class LogConfig:
    # Имя логгера
    logger_name = 'ApiSpbStuRuz'
    # Уровень отладки
    logging_level = logging.DEBUG
    # Название файла отладки
    __log_file_name = f'log/log-{datetime.datetime.now().strftime("%Y%m%d-%H%M%S%f")}.txt'
    log_handler = logging.FileHandler(__log_file_name, mode='w')
    # Формат вывода в отладчик
    __log_formatter = logging.Formatter('%(name)s %(asctime)s %(levelname)s %(message)s')
    log_handler.setFormatter(__log_formatter)
