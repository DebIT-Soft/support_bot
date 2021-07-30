# -*- coding: utf-8 -*-
import sys
from contextlib import ContextDecorator

import pymysql

# region Инициализация подключения, вход в текущее и закрытие
class get_connection(ContextDecorator):
    def __init__(self):
        try:
            self.data_base_connection = ''
        except:
            print('\033[31mERR >\033[0m __init__')

    def __enter__(self):
        try:
            self.data_base_connection = pymysql.connect(host='209.209.40.83',
                                                    port=39305,
                                                    user='admin',
                                                    password='lQTjDmJ1', 
                                                    db='tg_db',
                                                    charset='utf8mb4',
                                                    cursorclass=pymysql.cursors.DictCursor)
            # __cursor = self.data_base_connection.cursor()
            __cursor = self.data_base_connection
            
            return __cursor
        except pymysql.Error as err:
            print('\033[31mERR >\033[0m __enter__\n\n' + str(err))

    def __exit__(self, *exc):
        try:
            self.data_base_connection.commit()
            self.data_base_connection.close()
            return False
        except:
            print('\033[31mERR >\033[0m __exit__')
# endregion