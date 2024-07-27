# -*- coding: utf-8 -*-
from argon2.exceptions import VerifyMismatchError
from .md_database_manager import DataBaseManager
from .md_log_manager import LogManager
from argon2 import PasswordHasher
from datetime import datetime
from psycopg2 import sql
from flet import Page
import psycopg2

class Credentials:
    def __init__(self, page:Page, credential_id=None, user_id=None, password=None, last_login=None, failed_attempts=None,
                 is_user_locked=None, lockout_time=None, email=None):
        self.logger = LogManager()
        self.ph = PasswordHasher()
        self.page = page

        if credential_id is not None:
            data = self.read_credential(credential_id=credential_id)[0]
            self.credential_id = data[0]
            self.user_id = data[1]
            self.password = data[2]
            self.last_login = data[3]
            self.failed_attempts = data[4]
            self.is_user_locked = data[5]
            self.lockout_time = data[6]
            self.created_at = data[7]
            self.created_by = data[8]
            self.updated_at = data[9]
            self.email = data[10]
            return

        self.credential_id = credential_id
        self.user_id = user_id
        self.password = password
        self.last_login = last_login
        self.failed_attempts = failed_attempts
        self.is_user_locked = is_user_locked
        self.lockout_time = lockout_time
        self.created_at = None
        self.created_by = self.page.session.get('logged_user_id')
        self.updated_at = None
        self.email = email

    def check_login(self, email, password):
        with DataBaseManager() as conn:
            c = conn.cursor()
            c.execute(f"SELECT EXISTS (SELECT 1 FROM credentials WHERE login_email = '{email}')")
            email_exists = c.fetchone()[0]
            c.close()

        if not email_exists:
            self.logger.log_warning(f'Acesso negado pois email fornecido não é de nenhum usuário cadastrado no sistema')
            return -1

        with DataBaseManager() as conn:
            c = conn.cursor()
            c.execute(f"SELECT is_user_locked FROM credentials WHERE login_email = '{email}'")
            is_locked = c.fetchone()[0]
            c.close()

        if is_locked:
            self.logger.log_warning(f'Login negado para [{email}] - Usuário bloqueado')
            return -2

        with DataBaseManager() as conn:
            c = conn.cursor()
            c.execute(f"SELECT hashed_password FROM credentials WHERE login_email = '{email}'")
            hash = c.fetchone()[0]
            c.close()

        try:
            login = self.ph.verify(hash, password)

            with DataBaseManager() as conn:
                c = conn.cursor()
                c.execute(f'''
                    UPDATE credentials 
                    SET last_login = '{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}' 
                    WHERE login_email = '{email}'
                ''')
                conn.commit()
                c.close()

            return login
        except VerifyMismatchError as e:
            self.logger.log_warning(f"Login negado para [{email}] - Senha incorreta")

            with DataBaseManager() as conn:
                c = conn.cursor()
                c.execute(f'''
                    UPDATE credentials 
                    SET failed_attempts = (failed_attempts + 1) 
                    WHERE login_email = '{email}'
                ''')
                conn.commit()

                c.execute(f"SELECT failed_attempts FROM credentials WHERE login_email = '{email}'")
                failled_attempts = c.fetchone()[0]

                if failled_attempts >= 3:
                    c.execute(f"UPDATE credentials SET is_user_locked = TRUE WHERE login_email = '{email}'")
                    c.execute(f'''
                        UPDATE credentials 
                        SET lockout_time = '{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}' 
                        WHERE login_email = '{email}'
                    ''')
                    conn.commit()
                c.close()
            return False

    def do_already_exists(self, login):
        with DataBaseManager() as conn:
            c = conn.cursor()
            c.execute(f"SELECT EXISTS(SELECT 1 FROM credentials WHERE login_email = '{login}')")
            email_exists = c.fetchone()[0]
            c.close()

        if email_exists:
            return True
        return False

    def create_credential(self):
        with DataBaseManager() as conn:
            c = conn.cursor()
            c.execute(f"SELECT EXISTS(SELECT 1 FROM credentials WHERE user_id = {self.user_id})")
            user_exists = c.fetchone()[0]

            c.execute(f"SELECT EXISTS(SELECT 1 FROM credentials WHERE login_email = '{self.email}')")
            email_exists = c.fetchone()[0]
            c.close()

        if user_exists:
            self.logger.log_warning("Negada tentativa de criação de credencial, pois usuário fornecido já a possui")
            return -1

        if email_exists:
            self.logger.log_warning("Negada tentativa de criação de credencial, pois email fornecido já está "
                                    "cadastrado para outro usuário")
            return -2

        try:
            data = {
                'user_id': self.user_id,
                'hashed_password': self.ph.hash(self.password),
                'created_by': self.created_by,
                'login_email': self.email
            }

            table_name = 'credentials'
            columns = data.keys()
            values = data.values()

            query = sql.SQL("INSERT INTO {} ({}) VALUES ({}) RETURNING credential_id").format(
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
                self.credential_id = result
                self.logger.log_info(message=f'Nova CREDENCIAL criada [ID {self.credential_id}]')
                return self.credential_id
            return False
        except (BaseException, psycopg2.DatabaseError) as e:
            self.logger.log_error(message=f'Erro ao criar nova CREDENCIAL [{str(e)}]')
            return False

    def read_credential(self, columns='*', credential_id=None, condition=None):
        try:
            query = f'SELECT {columns} FROM credentials'
            query += f' WHERE credential_id = {credential_id}' if (credential_id is not None
                                                                   and condition is None) else ''
            query += f' WHERE {condition}' if condition is not None else ''

            with DataBaseManager() as conn:
                c = conn.cursor()
                c.execute(query)
                data = c.fetchall()
                c.close()

            return data
        except (BaseException, psycopg2.DatabaseError) as e:
            self.logger.log_error(f"Erro ao ler valores de CREDENCIAIS [{columns}] ID=[{credential_id}] "
                                  f"Condição=[{condition}] - [{str(e)}]")

    def update_credential(self, update_password=True, credencial_id=None, new_credential=None,
                          email=None, column_to_update=None, new_value=None):
        try:
            query = None
            query_update_at = None

            if update_password and (credencial_id is not None):
                query = (f"UPDATE credentials SET hashed_password = {self.ph.hash(new_credential)} "
                         f"WHERE credential_id = {credencial_id}")
                query_update_at = (
                    f"UPDATE credentials SET updated_at = '{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}' "
                    f"WHERE credential_id = {credencial_id}")
            elif update_password and (email is not None):
                query = (f"UPDATE credentials SET hashed_password = {self.ph.hash(new_credential)} "
                         f"WHERE login_email = '{email}'")
                query_update_at = (
                    f"UPDATE credentials SET updated_at = '{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}' "
                    f"WHERE login_email = '{email}'")
            elif credencial_id is not None:
                query = (f"UPDATE credentials SET {column_to_update} = {new_value} "
                         f"WHERE credential_id = {credencial_id}")
            else:
                query = (f"UPDATE credentials SET {column_to_update} = {new_value} "
                         f"WHERE login_email = '{email}'")

            with DataBaseManager() as conn:
                c = conn.cursor()
                c.execute(query)
                if query_update_at is not None:
                    c.execute(query_update_at)
                conn.commit()
                c.close()
            if query_update_at is not None:
                self.logger.log_info(f'SENHA [{credencial_id}] alterada')
            return True
        except (BaseException, psycopg2.DatabaseError) as e:
            self.logger.log_error(f"Erro ao alterar SENHA [{credencial_id}] - [{str(e)}]")

    def delete_credential(self, credential_id):
        try:
            query = f'''
                        DELETE FROM credentials WHERE credential_id = {credential_id}
                    '''

            with DataBaseManager() as conn:
                c = conn.cursor()
                c.execute(query)
                conn.commit()
                c.close()

            self.logger.log_info(f"CREDENCIAL [{credential_id}] excluida")
            return True
        except (BaseException, psycopg2.DatabaseError) as e:
            self.logger.log_error(f"Erro ao excluir CREDENCIAL [{credential_id}] - [{str(e)}]")


