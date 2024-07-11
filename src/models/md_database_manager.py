# -*- coding: utf-8 -*-
from dotenv import load_dotenv
from os import getenv
import psycopg2


class DataBaseManager:
    def __init__(self):
        load_dotenv()
        self.__dbname = getenv('DBNAME')
        self.__host = getenv('HOST')
        self.__user = getenv('USER')
        self.__password = getenv('PASSWORD')
        self.__port = getenv('PORT')
        self.__conn = None

    def __connect(self):
        if not self.__conn:
            try:
                self.__conn = psycopg2.connect(f"dbname={self.__dbname} "
                                               f"user={self.__user} "
                                               f"host={self.__host} "
                                               f"password={self.__password} "
                                               f"port={self.__port}")
            except BaseException as e:
                print(f"Erro ao conectar ao banco de dados {e}")

    def __disconnect(self):
        if self.__conn:
            self.__conn.close()
            self.__conn = None

    def __enter__(self):
        self.__connect()
        return self.__conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__disconnect()
