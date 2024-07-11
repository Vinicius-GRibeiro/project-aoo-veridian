# -*- coding: utf-8 -*-
from .md_database_manager import DataBaseManager
from .md_log_manager import LogManager
from psycopg2 import sql
from flet import Page
import psycopg2


class DocAvailability:
    def __init__(self, page: Page, doctor_id=None, aval_id=None, aval_date=None, aval_hour=None):
        self.logger = LogManager()
        self.page = page

        if aval_id is not None:
            data = self.read_availability(aval_id=aval_id)[0]
            self.aval_id = data[0]
            self.doctor_id = data[1]
            self.aval_date = data[2]
            self.aval_hour = data[3]
            self.is_available = data[4]
            self.created_at = data[5]
            self.created_by = data[6]

            return

        self.doctor_id = doctor_id
        self.aval_id = aval_id
        self.aval_date = aval_date
        self.aval_hour = aval_hour
        self.created_by = self.page.session.get('logged_user_id')

        self.created_at = None

    def create_availability(self):
        try:
            data = {
                'doctor_id': self.doctor_id,
                'aval_date': self.aval_date,
                'aval_hour': self.aval_hour,
                'created_by': self.created_by
            }

            table_name = 'doctors_availability'
            columns = data.keys()
            values = data.values()

            query = sql.SQL("INSERT INTO {} ({}) VALUES ({}) RETURNING aval_id").format(
                sql.Identifier(table_name),
                sql.SQL(', ').join(map(sql.Identifier, columns)),
                sql.SQL(', ').join(sql.Placeholder() * len(columns))
            )

            with DataBaseManager() as conn:
                c = conn.cursor()
                c.execute(query, list(values))
                result = c.fetchone()
                conn.commit()
                c.close()

            if result:
                self.aval_id = result
                self.logger.log_info(message=f'Nova DISPONIBILIDADE MÉDICA criada [ID {self.aval_id}]')
                return self.aval_id
            return False
        except (BaseException, psycopg2.DatabaseError) as e:
            self.logger.log_error(message=f'Erro ao criar nova DISPONIBILIDADE MÉDICA [{str(e)}]')
            return False

    def read_availability(self, columns='*', aval_id=None, condition=None):
        try:
            query = f'SELECT {columns} FROM doctors_availability'
            query += f' WHERE aval_id = {aval_id}' if aval_id is not None and condition is None else ''
            query += f' WHERE {condition}' if condition is not None else ''

            with DataBaseManager() as conn:
                c = conn.cursor()
                c.execute(query)
                data = c.fetchall()
                c.close()

            return data
        except (BaseException, psycopg2.DatabaseError) as e:
            self.logger.log_error(f"Erro ao ler valores de DISPONIBILIDADED_MÉDICA [{columns}] ID=[{aval_id}] "
                                  f"Condição=[{condition}] - [{str(e)}]")

    def update_availability(self, aval_id, new_value):
        new_value_name = 'DISPONÍVEL' if new_value else 'INDISPONÍVEL'

        try:
            query = f'''
                UPDATE doctors_availability SET is_available = {new_value} WHERE aval_id = {aval_id};
            '''

            with DataBaseManager() as conn:
                c = conn.cursor()
                c.execute(query)
                conn.commit()
                c.close()
                self.logger.log_info(f"DISPONIBILIDADE MÉDICA [{aval_id}] alterada para {new_value_name}")
                return True
        except (BaseException, psycopg2.DatabaseError) as e:
            self.logger.log_error(f'Erro ao mudar DISPONIBILIDADE MÉDICA [{aval_id}] para {new_value_name} '
                                  f'- [{str(e)}]')

    def delete_availability(self, aval_id):
        try:
            query = f'''
                DELETE FROM doctors_availability WHERE aval_id = {aval_id}
            '''

            with DataBaseManager() as conn:
                c = conn.cursor()
                c.execute(query)
                conn.commit()
                c.close()

            self.logger.log_info(f'DISPONIBILIDADE MÉDICA [{aval_id}] foi excluida')
            return True
        except (BaseException, psycopg2.DatabaseError) as e:
            self.logger.log_error(f'Erro ao excluir DISPONIBILIDADE MÉDICA [{aval_id}] - [{e}]')
            return False

