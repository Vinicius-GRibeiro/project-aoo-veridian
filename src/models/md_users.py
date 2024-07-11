# -*- coding: utf-8 -*-
from .md_database_manager import DataBaseManager
from .md_log_manager import LogManager
from psycopg2 import sql
from flet import Page
import psycopg2


class User:
    def __init__(self, page: Page=None, cpf=None, fullname=None, birth_date=None, phone_1=None, email=None, zipcode=None,
                 street=None, number=None, neighborhood=None, city=None, state=None, country=None, user_type=None,
                 gender=None, phone_2=None, complement=None, comments=None, user_id=None):

        # Logger object
        self.logger = LogManager()

        self.page = page

        # Verify if the object should create a new user or read an existent user from db and create the object by
        # __init__ filled parameters
        if user_id is not None:
            dados = self.read_user(user_id=user_id, columns='''
                                        cpf, fullname, birthdate, gender, phone_1, phone_2, email, address_zipcode,
                                        address_street, address_number,address_neighborhood, address_city,address_state,
                                        address_country, address_complement, comments,user_type, created_by,
                                        user_status, created_at'''
                                   )[0]

            self.user_id = user_id
            self.cpf = dados[0]
            self.fullname = dados[1]
            self.birth_date = dados[2]
            self.gender = dados[3]
            self.phone_1 = dados[4]
            self.phone_2 = dados[5]
            self.email = dados[6]
            self.address_zip_code = dados[7]
            self.address_street = dados[8]
            self.address_number = dados[9]
            self.address_neighborhood = dados[10]
            self.address_city = dados[11]
            self.address_state = dados[12]
            self.address_country = dados[13]
            self.address_complement = dados[14]
            self.comments = dados[15]
            self.user_type = dados[16]
            self.created_by = dados[17]

            self.user_status = dados[18]
            self.created_at = dados[19]

            return

        # If this is executed, the object will be created with given data from the user, not from the db.
        # Normal attributes. Can be consulted and set freely
        self.cpf = cpf
        self.fullname = fullname
        self.birth_date = birth_date
        self.gender = gender
        self.phone_1 = phone_1
        self.phone_2 = phone_2
        self.email = email
        self.address_zip_code = zipcode
        self.address_street = street
        self.address_number = number
        self.address_neighborhood = neighborhood
        self.address_city = city
        self.address_state = state
        self.address_country = country
        self.address_complement = complement
        self.comments = comments
        self.user_type = user_type
        self.created_by = 0  # self.page.session.get('logged_user_id')

        # Can be set, but isn't necessary
        self.user_status = None

        # Can be consulted but NEVER set, in this part of the code. Just for reading
        self.user_id = user_id
        self.created_at = None

    def _create_user(self):
        try:
            data = {
                'cpf': self.cpf,
                'fullname': self.fullname,
                'birthdate': self.birth_date,
                'gender': self.gender,
                'phone_1': self.phone_1,
                'phone_2': self.phone_2,
                'email': self.email,
                'address_zipcode': self.address_zip_code,
                'address_street': self.address_street,
                'address_number': self.address_number,
                'address_neighborhood': self.address_neighborhood,
                'address_city': self.address_city,
                'address_state': self.address_state,
                'address_country': self.address_country,
                'address_complement': self.address_complement,
                'created_by': -1,
                'comments': self.comments,
                'user_type': self.user_type
            }

            table_name = 'users'
            columns = data.keys()
            values = data.values()

            query = sql.SQL("INSERT INTO {} ({}) VALUES ({}) RETURNING user_id, created_at").format(
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
                self.user_id, self.created_at = result
                self.logger.log_info(message=f'Novo USUÁRIO criado [ID {self.user_id}]')
                return self.user_id
            return False
        except (BaseException, psycopg2.DatabaseError) as e:
            self.logger.log_error(message=f'Erro ao criar novo USUÁRIO [{str(e)}]')
            return False

    def read_user(self, columns='*', user_id=None, condition=None, order_by=None):
        try:
            query = f'SELECT {columns} FROM users'
            query += f' WHERE user_id = {user_id}' if user_id is not None and condition is None else ''
            query += f' WHERE {condition}' if condition is not None else ''
            query += f' ORDER BY {order_by}' if order_by is not None else ''

            with DataBaseManager() as conn:
                c = conn.cursor()
                c.execute(query)
                data = c.fetchall()
                c.close()

            return data
        except (BaseException, psycopg2.DatabaseError) as e:
            self.logger.log_error(f"Erro ao ler valores de USUÁRIOS [{columns}] ID=[{user_id}] Condição=[{condition}] "
                                  f"- [{str(e)}]")

    def update_user(self, user_id, columns, new_values):
        try:
            set_clause = sql.SQL(', ').join(
                sql.Composed([sql.Identifier(col), sql.SQL(" = %s")]) for col in columns
            )
            query = sql.SQL("UPDATE users SET {set_clause} WHERE user_id = %s").format(
                set_clause=set_clause
            )
            new_values.append(user_id)

            with DataBaseManager() as conn:
                c = conn.cursor()
                c.execute(query, new_values)
                conn.commit()
                c.close()
                self.logger.log_info(f"Atualização do USUÁRIO - {columns} para ID={new_values[::-1]}")
                return True
        except (BaseException, psycopg2.DatabaseError) as e:
            self.logger.log_error(f'Erro ao editar dados do USUÁRIO [{user_id}] - [{str(e)}]')

    def _delete_user(self, user_id):
        try:
            query = sql.SQL("DELETE FROM users WHERE user_id = %s")

            with DataBaseManager() as conn:
                c = conn.cursor()
                c.execute(query, (user_id,))
                conn.commit()
                c.close()
                self.logger.log_info(f"USUÁRIO deletado [ID={user_id}]")
            return True
        except (BaseException, psycopg2.DatabaseError) as e:
            self.logger.log_error(f"Erro ao excluir USUÁRIO [{user_id}] - [{e}")
            return False


class Doctor(User):
    def __init__(self, page: Page, cpf=None, fullname=None, birth_date=None, phone_1=None, email=None, zipcode=None, street=None,
                 number=None, neighborhood=None, city=None, state=None, country=None, user_type='médico',
                 created_by=None, gender=None, phone_2=None, complement=None, comments=None, user_id=None,
                 crm=None, specialty=None, price=None):
        super().__init__(page, cpf, fullname, birth_date, phone_1, email, zipcode, street, number, neighborhood,
                         city, state, country, user_type, created_by, gender, phone_2, complement, comments, user_id)

        if user_id is not None:
            data = self.read_doctor(user_id=user_id)[0]
            self.user_id = data[0]
            self.crm = data[1]
            self.specialty = data[2]
            self.price = data[3]
            return

        self.crm = crm
        self.specialty = specialty
        self.price = price

    def create_doctor(self):
        doc_id = self._create_user()

        if not doc_id:
            return False

        try:
            data = {
                'user_id': doc_id,
                'crm': self.crm,
                'specialty': self.specialty,
                'price': self.price,
            }

            table_name = 'doctors'
            columns = data.keys()
            values = data.values()

            query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                sql.Identifier(table_name),
                sql.SQL(', ').join(map(sql.Identifier, columns)),
                sql.SQL(', ').join(sql.Placeholder() * len(columns))
            )

            with DataBaseManager() as conn:
                cur = conn.cursor()
                cur.execute(query, list(values))
                conn.commit()
                cur.close()

            self.logger.log_info(message=f'Novo MÉDICO criado [ID {self.user_id}]')
            return True
        except (BaseException, psycopg2.DatabaseError) as e:
            self.logger.log_error(message=f'Erro ao criar MÉDICO [{str(e)}]')
            return False

    def read_doctor(self, columns='*', user_id=None, condition=None):
        try:
            query = f'SELECT {columns} FROM doctors'
            query += f' WHERE user_id = {user_id}' if user_id is not None and condition is None else ''
            query += f' WHERE {condition}' if condition is not None else ''

            with DataBaseManager() as conn:
                c = conn.cursor()
                c.execute(query)
                data = c.fetchall()
                c.close()

            return data
        except (BaseException, psycopg2.DatabaseError) as e:
            self.logger.log_error(f"Erro ao ler valores [{columns}] ID=[{user_id}] Condição=[{condition}] - [{str(e)}]")

    def update_doctor(self, user_id, columns, new_values):
        try:
            set_clause = sql.SQL(', ').join(
                sql.Composed([sql.Identifier(col), sql.SQL(" = %s")]) for col in columns
            )
            query = sql.SQL("UPDATE doctors SET {set_clause} WHERE user_id = %s").format(
                set_clause=set_clause
            )
            new_values.append(user_id)

            with DataBaseManager() as conn:
                c = conn.cursor()
                c.execute(query, new_values)
                conn.commit()
                c.close()
                self.logger.log_info(f"Atualização do MÉDICO - {columns} para ID={new_values[::-1]}")
                return True
        except (BaseException, psycopg2.DatabaseError) as e:
            self.logger.log_error(f'Erro ao editar dados do MÉDICO [{user_id}] - [{str(e)}]')

    def delete_doctor(self, user_id):
        try:
            query = sql.SQL("DELETE FROM doctors WHERE user_id = %s")

            with DataBaseManager() as conn:
                c = conn.cursor()
                c.execute(query, (user_id,))
                conn.commit()
                c.close()
                self.logger.log_info(f"MÉDICO deletado [ID={user_id}]")

            return self._delete_user(user_id)
        except (BaseException, psycopg2.DatabaseError) as e:
            self.logger.log_error(f"Erro ao excluir MÉDICO [{user_id}] - [{e}")
            return False


class Patient(User):
    def __init__(self, page: Page, cpf=None, fullname=None, birth_date=None, phone_1=None, email=None, zipcode=None, street=None,
                 number=None, neighborhood=None, city=None, state=None, country=None, user_type='paciente',
                 created_by=None, gender=None, phone_2=None, complement=None, comments=None, user_id=None,
                 insurance=None):
        super().__init__(page, cpf, fullname, birth_date, phone_1, email, zipcode, street, number, neighborhood,
                         city, state, country, user_type, created_by, gender, phone_2, complement, comments, user_id)

        if user_id is not None:
            data = self.read_patient(user_id=user_id)[0]
            self.insurance = data[1]
            return

        self.insurance = insurance

    def create_patient(self):
        patient_id = self._create_user()

        if not patient_id:
            return False

        try:
            data = {
                'user_id': patient_id,
                'insurance': self.insurance
            }

            table_name = 'patients'
            columns = data.keys()
            values = data.values()

            query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                sql.Identifier(table_name),
                sql.SQL(', ').join(map(sql.Identifier, columns)),
                sql.SQL(', ').join(sql.Placeholder() * len(columns))
            )

            with DataBaseManager() as conn:
                cur = conn.cursor()
                cur.execute(query, list(values))
                conn.commit()
                cur.close()

            self.logger.log_info(message=f'Novo PACIENTE criado [ID {self.user_id}]')
            return True
        except (BaseException, psycopg2.DatabaseError) as e:
            self.logger.log_error(message=f'Erro ao criar PACIENTE [{str(e)}]')
            return False

    def read_patient(self, columns='*', user_id=None, condition=None):
        try:
            query = f'SELECT {columns} FROM patients'
            query += f' WHERE user_id = {user_id}' if user_id is not None and condition is None else ''
            query += f' WHERE {condition}' if condition is not None else ''

            with DataBaseManager() as conn:
                c = conn.cursor()
                c.execute(query)
                data = c.fetchall()
                c.close()

            return data
        except (BaseException, psycopg2.DatabaseError) as e:
            self.logger.log_error(f"Erro ao ler valores [{columns}] ID=[{user_id}] Condição=[{condition}] - [{str(e)}]")

    def update_patient(self, user_id, columns, new_values):
        try:
            set_clause = sql.SQL(', ').join(
                sql.Composed([sql.Identifier(col), sql.SQL(" = %s")]) for col in columns
            )
            query = sql.SQL("UPDATE patients SET {set_clause} WHERE user_id = %s").format(
                set_clause=set_clause
            )
            new_values.append(user_id)

            with DataBaseManager() as conn:
                c = conn.cursor()
                c.execute(query, new_values)
                conn.commit()
                c.close()
                self.logger.log_info(f"Atualização do PACIENTE - {columns} para ID={new_values[::-1]}")
                return True
        except (BaseException, psycopg2.DatabaseError) as e:
            self.logger.log_error(f'Erro ao editar dados do PACIENTE [{user_id}] - [{str(e)}]')

    def delete_patient(self, user_id):
        try:
            query = sql.SQL("DELETE FROM patients WHERE user_id = %s")

            with DataBaseManager() as conn:
                c = conn.cursor()
                c.execute(query, (user_id,))
                conn.commit()
                c.close()
                self.logger.log_info(f"PACIENTE deletado [ID={user_id}]")

            return self._delete_user(user_id)
        except (BaseException, psycopg2.DatabaseError) as e:
            self.logger.log_error(f"Erro ao excluir PACIENTE [{user_id}] - [{e}")
            return False


class Employee(User):
    def __init__(self, page: Page, cpf=None, fullname=None, birth_date=None, phone_1=None, email=None, zipcode=None, street=None,
                 number=None, neighborhood=None, city=None, state=None, country=None, user_type='funcionário',
                 created_by=None, gender=None, phone_2=None, complement=None, comments=None, user_id=None,
                 role=None):
        super().__init__(page, cpf, fullname, birth_date, phone_1, email, zipcode, street, number, neighborhood,
                         city, state, country, user_type, created_by, gender, phone_2, complement, comments, user_id)
        self.role = role

    def create_employee(self):
        employee_id = self._create_user()

        if not employee_id:
            return False

        try:
            data = {
                'user_id': employee_id,
                'role': self.role
            }

            table_name = 'employees'
            columns = data.keys()
            values = data.values()

            query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                sql.Identifier(table_name),
                sql.SQL(', ').join(map(sql.Identifier, columns)),
                sql.SQL(', ').join(sql.Placeholder() * len(columns))
            )

            with DataBaseManager() as conn:
                cur = conn.cursor()
                cur.execute(query, list(values))
                conn.commit()
                cur.close()

            self.logger.log_info(message=f'Novo FUNCIONÁRIO criado [ID {self.user_id}]')
            return True
        except (BaseException, psycopg2.DatabaseError) as e:
            self.logger.log_error(message=f'Erro ao criar FUCIONÁRIO [{str(e)}]')
            return False

    def read_employee(self, columns='*', user_id=None, condition=None):
        try:
            query = f'SELECT {columns} FROM employees'
            query += f' WHERE user_id = {user_id}' if user_id is not None and condition is None else ''
            query += f' WHERE {condition}' if condition is not None else ''

            with DataBaseManager() as conn:
                c = conn.cursor()
                c.execute(query)
                data = c.fetchall()
                c.close()

            return data
        except (BaseException, psycopg2.DatabaseError) as e:
            self.logger.log_error(f"Erro ao ler valores [{columns}] ID=[{user_id}] Condição=[{condition}] - [{str(e)}]")

    def update_employee(self, user_id, columns, new_values):
        try:
            set_clause = sql.SQL(', ').join(
                sql.Composed([sql.Identifier(col), sql.SQL(" = %s")]) for col in columns
            )
            query = sql.SQL("UPDATE employees SET {set_clause} WHERE user_id = %s").format(
                set_clause=set_clause
            )
            new_values.append(user_id)

            with DataBaseManager() as conn:
                c = conn.cursor()
                c.execute(query, new_values)
                conn.commit()
                c.close()
                self.logger.log_info(f"Atualização do funcionário - {columns} para ID={new_values[::-1]}")
                return True
        except (BaseException, psycopg2.DatabaseError) as e:
            self.logger.log_error(f'Erro ao editar dados do funcionário [{user_id}] - [{str(e)}]')

    def delete_employee(self, user_id):
        try:
            query = sql.SQL("DELETE FROM employees WHERE user_id = %s")

            with DataBaseManager() as conn:
                c = conn.cursor()
                c.execute(query, (user_id,))
                conn.commit()
                c.close()
                self.logger.log_info(f"Funcionário deletado [ID={user_id}]")

            return self._delete_user(user_id)
        except (BaseException, psycopg2.DatabaseError) as e:
            self.logger.log_error(f"Erro ao excluir funcionário [{user_id}] - [{e}")
            return False
