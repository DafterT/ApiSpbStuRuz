"""
A file with settings for the logger.
Here the need for logging, the folder with logs, the format of logs, etc. is established.

Date of create file: 01.29.2023
"""

import logging
import datetime
import os


class LogConfig:
    # Уровень отладки
    # logging_level = logging.DEBUG
    logging_level = logging.CRITICAL + 1  # Для отключения логирования
    # Создали заглушки
    logger_name = None
    log_handler = None
    # Проверили что логи необходимо вести
    if logging_level <= logging.CRITICAL:
        # Имя логгера
        logger_name = 'ApiSpbStuRuz'
        # Создание папки log
        if not os.path.exists('log'):
            os.makedirs('log')
        # Название файла отладки
        __log_file_name = f'log/log-{datetime.datetime.now().strftime("%Y%m%d-%H%M%S%f")}.txt'
        log_handler = logging.FileHandler(__log_file_name, mode='w')
        # Формат вывода в отладчик
        __log_formatter = logging.Formatter('%(name)s %(asctime)s %(levelname)s %(message)s')
        log_handler.setFormatter(__log_formatter)
