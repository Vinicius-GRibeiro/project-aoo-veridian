# -*- coding: utf-8 -*-
from flet import *
from src.controls.gui_utils import notify
from src.models.md_credentials import Credentials
from src.models.md_users import User
from fletmint import TextInput


class Btn:
    def __init__(self, page: Page, text: str, email_input: TextInput, password_input=TextInput):
        self.page = page
        self.email_input = email_input
        self.password_input = password_input

        self.get = TextButton(
            content=Container(Text(value=text, color=colors.ON_PRIMARY, size=18, font_family='nunito2'),
                              padding=padding.symmetric(5, 20)),
            style=ButtonStyle(
                bgcolor=colors.PRIMARY,
                color=colors.ON_PRIMARY,
            ),
            on_click=lambda e: self.click()
        )

    def click(self):

        email = self.email_input
        password = self.password_input

        def reset_fields(email=None, password=None):
            if email is not None:
                email.text_field.value = ''
            if password is not None:
                password.text_field.value = ''

            self.page.update()

        if email.text_field.value == '' or password.text_field.value == '':
            notify(self.page, 'Os campos de email e senha não podem estar vazios', icon=icons.WARNING_ROUNDED)
            return

        is_approved = Credentials(self.page).check_login(email=email.text_field.value,
                                                         password=password.text_field.value)

        if is_approved == -1:
            notify(self.page, 'E-mail não cadastrado no sistema', icon=icons.WARNING_ROUNDED)
            reset_fields(password)
            return

        if is_approved == -2:
            notify(self.page, 'Usuário bloqueado. Consulte seu gerente', icon=icons.PERSON_OFF_ROUNDED)
            reset_fields(password)
            return

        if not is_approved:
            attempts = Credentials(self.page).read_credential(columns='failed_attempts',
                                                              condition=f"login_email='{email.text_field.value}'")
            remaining_attempts = (3 - attempts[0][0]) if attempts is not None else 'NaN'

            message = (f'Senha inserida não corresponde a senha cadastrada para esse e-mail\n'
                       f'Cuidado! Tentativas restantes: {remaining_attempts}') if remaining_attempts > 0 else (
                f"Seu usuário foi bloqueado por muitas tentativas de login"
            )

            notify(self.page, message, icon=icons.WARNING_ROUNDED)
            reset_fields(password)
            return

        Credentials(self.page).update_credential(update_password=False, email=email.text_field.value,
                                                 column_to_update='failed_attempts', new_value=0)

        logged_user_id = Credentials(self.page).read_credential(columns='user_id',
                                                                condition=f"login_email = '{email.text_field.value}'")

        if logged_user_id is not None:
            logged_user_id = logged_user_id[0][0]
            self.page.session.set('logged_user_id', logged_user_id)
            logged_user_type = User(user_id=logged_user_id).user_type
            if logged_user_type is not None:
                self.page.session.set('logged_user_type', logged_user_type)

        reset_fields(email, password)


class BtnText:
    def __init__(self, text: str):
        self.get = TextButton(
            content=Container(Text(value=text, color=colors.PRIMARY, size=15, font_family='nunito'),
                              padding=padding.symmetric(5, 20)),
            style=ButtonStyle(
                overlay_color='transparent'
            )
        )
