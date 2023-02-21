"""
A file with settings for the logger.
Here the need for logging, the folder with logs, the format of logs, etc. is established.

Date of create file: 01.29.2023
"""

import logging
import datetime
import os


class LogConfig:
    def __init__(self, create_logger=False, path_log='log/'):
        # Создали заглушки
        self.logger_name = None
        self.log_handler = None
        # Уровень отладки
        self.logging_level = logging.DEBUG if create_logger else logging.CRITICAL + 1
        # Проверили что логи необходимо вести
        if self.logging_level > logging.CRITICAL:
            return
        # Имя логгера
        self.logger_name = 'ApiSpbStuRuz'
        # Создание папки log
        if not os.path.exists(path_log):
            os.makedirs(path_log)
        # Название файла отладки
        log_file_name = f'{path_log}/log-{datetime.datetime.now().strftime("%Y%m%d-%H%M%S%f")}.txt'
        self.log_handler = logging.FileHandler(log_file_name, mode='w')
        # Формат вывода в отладчик
        log_formatter = logging.Formatter('%(name)s %(asctime)s %(levelname)s %(message)s')
        self.log_handler.setFormatter(log_formatter)

    def get_logger(self):
        logger = logging.getLogger(self.logger_name)
        logger.setLevel(self.logging_level)
        logger.addHandler(self.log_handler)
        return logger
