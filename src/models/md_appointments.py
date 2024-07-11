# -*- coding: utf-8 -*-
from src.controls.utils import convert_money_from_db_to_float_money
from .md_database_manager import DataBaseManager
from .md_log_manager import LogManager
from datetime import datetime
from md_users import Doctor
from psycopg2 import sql
from flet import Page
import psycopg2


PROFIT_PORC = 0.3


class Appointment:
    def __init__(self, page: Page, appointment_id=None, patient_id=None, doctor_id=None, date_aval_id=None):
        self.logger = LogManager()
        self.page = page

        if appointment_id is not None:
            data = self.read_appointment(appointment_id=appointment_id)[0]
            self.appointment_id = data[0]
            self.patient_id = data[1]
            self.doctor_id = data[2]
            self.date_aval_id = data[3]
            self.status = data[4]
            self.total_price = data[5]
            self.created_at = data[6]
            self.created_by = data[7]
            self.canceled_for = data[8]
            self.canceled_at = data[9]
            return

        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.date_aval_id = date_aval_id
        self.status = 'agendado'
        self.total_price = self.calculate_total_price(self.doctor_id) if patient_id is not None else None
        self.created_at = None
        self.created_by = self.page.session.get('logged_user_id')
        self.canceled_for = None
        self.canceled_at = None

    @staticmethod
    def calculate_total_price(doc_id):
        doc = Doctor(user_id=doc_id)
        doc_price_float = convert_money_from_db_to_float_money(doc.price)
        return doc_price_float + (doc_price_float * PROFIT_PORC)

    def create_appointment(self):
        try:
            data = {
                'pacient_id': self.patient_id,
                'doctor_id': self.doctor_id,
                'date_aval_id': self.date_aval_id,
                'total_price': self.total_price,
                'created_by': self.created_by
            }

            table_name = 'appointments'
            columns = data.keys()
            values = data.values()

            query = sql.SQL("INSERT INTO {} ({}) VALUES ({}) RETURNING appointment_id").format(
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
                self.appointment_id = result
                self.logger.log_info(message=f'Nova CONSULTA criada [ID {self.appointment_id}]')
                return self.appointment_id
            return False
        except (BaseException, psycopg2.DatabaseError) as e:
            self.logger.log_error(message=f'Erro ao criar nova CONSULTA [{str(e)}]')
            return False

    def read_appointment(self, columns='*', appointment_id=None, condition=None):
        try:
            query = f'SELECT {columns} FROM appointments'
            query += f' WHERE appointment_id = {appointment_id}' if (appointment_id is not None
                                                                     and condition is None) else ''
            query += f' WHERE {condition}' if condition is not None else ''

            with DataBaseManager() as conn:
                c = conn.cursor()
                c.execute(query)
                data = c.fetchall()
                c.close()

            return data
        except (BaseException, psycopg2.DatabaseError) as e:
            self.logger.log_error(f"Erro ao ler valores de AGENDAMENTOS [{columns}] ID=[{appointment_id}] "
                                  f"Condição=[{condition}] - [{str(e)}]")

    def update_appointment(self, appointment_id, status, canceled_for=None):
        params = [status]

        try:
            query = f"UPDATE appointments SET status = %s"

            if canceled_for is not None:
                query += ", canceled_for = %s, canceled_at = %s"
                params.append(canceled_for)
                params.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))

            query += " WHERE appointment_id = %s"
            params.append(appointment_id)

            with DataBaseManager() as conn:
                c = conn.cursor()
                c.execute(query, tuple(params))
                conn.commit()
                c.close()

            self.logger.log_info(f'status do AGENDAMENTO [{appointment_id}] alterado para {params}')
            return True
        except (BaseException, psycopg2.DatabaseError) as e:
            self.logger.log_error(f"Erro ao alterar status do AGENDAMENTO ID=[{appointment_id}] para {params} "
                                  f"- [{str(e)}]")

    def delete_appointment(self, appointment_id):
        try:
            query = f'''
                        DELETE FROM appointments WHERE appointment_id = {appointment_id}
                    '''

            with DataBaseManager() as conn:
                c = conn.cursor()
                c.execute(query)
                conn.commit()
                c.close()

            self.logger.log_info(f"AGENDAMENTO [{appointment_id}] excluido")
            return True
        except (BaseException, psycopg2.DatabaseError) as e:
            self.logger.log_error(f"Erro ao alterar excluir AGENDAMENTO ID=[{appointment_id}] - [{str(e)}]")
