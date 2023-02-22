"""
A file with settings for the logger.
Here the need for logging, the folder with logs, the format of logs, etc. is established.

Date of create file: 01.29.2023
"""

import logging
import datetime
import os


class LogConfig:
    """
    A class containing the logger settings and a function for creating it
    """

    def __init__(self, create_logger=False, path_log='log/', try_create_dict=True):
        """
        Init start configs for logger. Create directory, if you want.

        :param create_logger: if you want to use a logger, pass True, otherwise don't change.
        :param path_log: the path to the folder where the logger will write logs.
        Before using, do not forget to enable the logger.
        :param try_create_dict: If you want the logger not to try to create a folder with logs,
        then turn off this parameter.
        """
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
        if try_create_dict and not os.path.exists(path_log):
            os.makedirs(path_log)
        # Название файла отладки
        log_file_name = f'{path_log}/log-{datetime.datetime.now().strftime("%Y%m%d-%H%M%S%f")}.txt'
        self.log_handler = logging.FileHandler(log_file_name, mode='w')
        # Формат вывода в отладчик
        log_formatter = logging.Formatter('%(name)s %(asctime)s %(levelname)s %(message)s')
        self.log_handler.setFormatter(log_formatter)

    def get_logger(self):
        """
        :return: will return the logger.
        """
        logger = logging.getLogger(self.logger_name)
        logger.setLevel(self.logging_level)
        logger.addHandler(self.log_handler)
        return logger
