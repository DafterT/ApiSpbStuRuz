"""
A file with settings for the logger.
Here the need for logging, the folder with logs, the format of logs, etc. is established.

Date of create file: 01.29.2023
"""

import logging
import datetime
import os


class LogConfig:
    # Создали заглушки
    logger_name = None
    log_handler = None

    def __init__(self, create_logger=False, path_log='log/'):
        # Уровень отладки
        self.logging_level = logging.DEBUG if create_logger else logging.CRITICAL + 1
        # Проверили что логи необходимо вести
        if self.logging_level <= logging.CRITICAL:
            # Имя логгера
            self.logger_name = 'ApiSpbStuRuz'
            # Создание папки log
            if not os.path.exists('log'):
                os.makedirs('log')
            # Название файла отладки
            log_file_name = f'{path_log}/log-{datetime.datetime.now().strftime("%Y%m%d-%H%M%S%f")}.txt'
            self.log_handler = logging.FileHandler(log_file_name, mode='w')
            # Формат вывода в отладчик
            log_formatter = logging.Formatter('%(name)s %(asctime)s %(levelname)s %(message)s')
            self.log_handler.setFormatter(log_formatter)
