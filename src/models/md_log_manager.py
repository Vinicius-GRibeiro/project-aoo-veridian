# -*- coding: utf-8 -*-
import logging


class LogManager:
    def __init__(self, log_file="app.log"):
        self.__log_file = log_file
        self.__logger = logging.getLogger("AppLogger")
        self.__logger.setLevel(logging.DEBUG)

        if not self.__logger.hasHandlers():
            formatter = logging.Formatter('\n%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

            file_handler = logging.FileHandler(self.__log_file)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            self.__logger.addHandler(file_handler)

            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            console_handler.setFormatter(formatter)
            self.__logger.addHandler(console_handler)

    def log_info(self, message):
        self.__logger.info(message)

    def log_warning(self, message):
        self.__logger.warning(message)

    def log_error(self, message):
        self.__logger.error(message)
