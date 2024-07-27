# -*- coding: utf-8 -*-
import datetime
from flet import *
from ..components.menu.md_menu import Menu
from .vw_md_usuarios_novos import Txt, Choose, SearchCepButton, SimpleTextButton
from src.controls.ctrl_novos_usuarios import validate_cpf
from src.models.md_users import User

BORDER_RADIUS = 10
BORDER_COLORS = '#494D5F'
ROW_DEFAULT_SPACING = 10

VERTICAL_PAD = 10
HORIZONTAL_PAD = 20
ROW_DIVIDER_WIDTH = 15
COLUMN_SPACING = 7


class ViewUsuariosNovos:
    def __init__(self, page: Page):
        self.page = page

        self.dd_user_type = Choose(self.page, options=['funcionário', 'médico', 'paciente'], label='Tipo de usuário',
                                   width=150)
        self.dd_user_type.get.on_change = lambda e: self.__update_specific_controls(e)

        self.txt_fullname = Txt(self.page, label='Nome completo', width=510)
        self.txt_cpf = Txt(self.page, label='CPF', width=160, input_filter=NumbersOnlyInputFilter())
        self.badge_txt_cpf = Badge(content=self.txt_cpf.get, bgcolor='transparent')
        self.txt_cpf.get.on_change = lambda e: self.__on_cpf_change(e)

        self.dd_gender = Choose(self.page, options=['Masculino', 'Feminino', 'Outros', '-'], selected_value=None,
                                width=120, label='Gênero')
        self.txt_telephone_1 = Txt(self.page, label='Telefone 1', width=155)
        self.txt_telephone_2 = Txt(self.page, label='Telefone 2', width=155)
        self.txt_email = Txt(self.page, label='E-mail', width=245)
        self.birthdate_input = Container(
            content=Text('Data nasc.', text_align=TextAlign.CENTER, color=colors.PRIMARY, weight=FontWeight.W_600),
            border=border.all(2, BORDER_COLORS), border_radius=BORDER_RADIUS, width=125, bgcolor='#22242a',
            padding=padding.only(top=5, bottom=5, right=20, left=20),
            on_click=lambda e: self.page.open(self.__date_picker),
        )
        self.__date_picker = DatePicker(date_picker_entry_mode=DatePickerEntryMode.CALENDAR_ONLY,
                                        cancel_text='Cancelar',
                                        help_text='Escolha a data', on_change=lambda e: self.__fill_date_from_picker(e))

        self.txt_cep = Txt(self.page, label='CEP', width=160, input_filter=NumbersOnlyInputFilter())
        self.txt_street = Txt(self.page, label='Rua', width=510)
        self.txt_number = Txt(self.page, label='Número', width=107)

        self.txt_neighborhood = Txt(self.page, label='Bairro', width=300)
        self.txt_city = Txt(self.page, label='Cidade', width=300)
        self.txt_country = Txt(self.page, label='País', width=130)
        self.dd_state = Choose(self.page, label='UF', width=80, options=["AC", "AL", "AP", "AM", "BA", "CE", "DF",
                                                                         "ES", "GO", "MA", "MT", "MS",
                                                                         "MG", "PA", "PB", "PR", "PE", "PI", "RJ",
                                                                         "RN", "RS", "RO", "RR", "SC",
                                                                         "SP", "SE", "TO"])

        self.txt_complement = Txt(self.page, label='Complemento', width=840)

        self.txt_comments = Txt(self.page, label='Comentários', width=840)

        self.txt_created_by = Txt(self.page, label='Criado por', width=840, read_only=True)
        logged_user = User().read_user(columns='user_id, fullname', user_id=self.page.session.get('logged_user_id'))[0]
        self.txt_created_by.get.value = f"{logged_user[0]} - {logged_user[1]}"

        self.btn_search_cep = SearchCepButton(self.page, icon=icons.SEARCH, controls=[self.txt_cep,
                                                                                      self.txt_street,
                                                                                      self.txt_number,
                                                                                      self.txt_neighborhood,
                                                                                      self.txt_city,
                                                                                      self.txt_country,
                                                                                      self.dd_state])

        self.txt_login = Txt(self.page, label='Identificação', width=300)
        self.txt_password = Txt(self.page, label='Senha', width=300, password=True)
        self.txt_confirm_password = Txt(self.page, label='Confirmação de senha', width=300, password=True)

        self.specific_ensurance = Txt(self.page, label='Seguro - Convênio', width=300)
        self.specific_role = Txt(self.page, label='Cargo', width=300)
        self.specific_crm = Txt(self.page, label='CRM', width=300)
        self.specific_price = Txt(self.page, label='Preço Consulta - R$', width=300)
        self.specific_specialty = Choose(self.page, label='Especialidade', width=300,
                                         options=['angiologista', 'cardiologista', 'dentista', 'dermatologista',
                                                  'endocrinologista', 'fonoaudiólogo', 'geriatra', 'ginecologista',
                                                  'hematologista', 'nefrologista',
                                                  'neurologista', 'nutricionista', 'obstetricista', 'oftalmologista',
                                                  'oncologista', 'ortopedista',
                                                  'otorrinolaringologista', 'pediatra', 'psicólogo', 'pneumologista',
                                                  'proctologista', 'psiquiatra', 'reumatologista',
                                                  'urologista'])

        self.specific_data_column = Column(
            spacing=COLUMN_SPACING,
            controls=[
                Container(Text('DADOS ESPECÍFICOS', font_family='nunito2',
                               color=colors.PRIMARY),
                          padding=padding.only(bottom=10)),

                Container(height=ROW_DIVIDER_WIDTH)
            ]
        )

        controls_to_add = [self.dd_user_type.get,
                           self.txt_fullname.get,
                           self.txt_cpf.get,
                           self.dd_gender.get,
                           self.txt_telephone_1.get,
                           self.txt_telephone_2.get,
                           self.txt_email.get,
                           self.birthdate_input.content,
                           self.txt_cep.get,
                           self.txt_street.get,
                           self.txt_number.get,
                           self.txt_neighborhood.get,
                           self.txt_city.get,
                           self.txt_country.get,
                           self.dd_state.get,
                           self.txt_complement.get,
                           self.txt_comments.get,
                           self.txt_created_by.get,
                           self.txt_login.get,
                           self.txt_password.get,
                           self.txt_confirm_password.get,
                           self.specific_data_column.controls]

        self.btn_create_user = SimpleTextButton(self.page, text='Criar usuário', width=300, main_btn=True,
                                                controls=controls_to_add)

        self.menu_footer = Menu(self.page, selected_item='Usuários').get
        self.get_view = self._get_view()

    def __update_specific_controls(self, e: ControlEvent):
        self.specific_data_column.controls.clear()

        self.specific_data_column.controls.append(Container(Text('DADOS ESPECÍFICOS', font_family='nunito2',
                                                                 color=colors.PRIMARY),
                                                            padding=padding.only(bottom=10)))

        self.specific_data_column.controls.append(Container(height=ROW_DIVIDER_WIDTH))

        if e.data == 'médico':
            self.specific_data_column.controls.append(self.specific_crm.get)
            self.specific_data_column.controls.append(self.specific_price.get)
            self.specific_data_column.controls.append(self.specific_specialty.get)
        elif e.data == 'funcionário':
            self.specific_data_column.controls.append(self.specific_role.get)
        elif e.data == 'paciente':
            self.specific_data_column.controls.append(self.specific_ensurance.get)

        self.page.update()

    def __fill_date_from_picker(self, e: ControlEvent):
        date = datetime.datetime.strptime(e.data[:10:], '%Y-%m-%d').date()
        self.birthdate_input.content.value = date.strftime('%d/%m/%Y')
        self.page.update()

    def __on_cpf_change(self, e: ControlEvent):
        if len(self.txt_cpf.get.value) >= 11:
            is_cpf_valid = validate_cpf(self.txt_cpf.get.value)
            self.badge_txt_cpf.bgcolor = colors.GREEN if is_cpf_valid else colors.RED
        else:
            self.badge_txt_cpf.bgcolor = 'transparent'
        self.page.update()

    def _get_view(self) -> View:
        v = View(
            spacing=0,
            padding=0,
            bgcolor=self.page.session.get('bg_main_color_light'),
            controls=[
                Column(
                    spacing=20,
                    controls=[
                        Row(controls=[Menu(self.page, selected_item='Usuários').get]),  # Menu row

                        Row(  # Content row
                            controls=[
                                Container(width=ROW_DIVIDER_WIDTH),
                                Column(  # Form column
                                    controls=[
                                        Container(
                                            border=border.only(left=BorderSide(5, colors.PRIMARY)),
                                            padding=padding.only(top=VERTICAL_PAD, left=HORIZONTAL_PAD,
                                                                 right=HORIZONTAL_PAD, bottom=VERTICAL_PAD),
                                            content=Column(
                                                spacing=COLUMN_SPACING,
                                                controls=[
                                                    Container(Text('DADOS PESSOAIS', font_family='nunito2',
                                                                   color=colors.PRIMARY),
                                                              padding=padding.only(bottom=10)),
                                                    Row(spacing=ROW_DEFAULT_SPACING,
                                                        controls=[self.dd_user_type.get, self.badge_txt_cpf,
                                                                  self.txt_fullname.get]),
                                                    Row(spacing=ROW_DEFAULT_SPACING,
                                                        controls=[self.dd_gender.get, self.birthdate_input,
                                                                  self.txt_telephone_1.get, self.txt_telephone_2.get,
                                                                  self.txt_email.get,
                                                                  ])
                                                ]
                                            )
                                        ),
                                        Container(height=ROW_DIVIDER_WIDTH),
                                        Container(
                                            border=border.only(left=BorderSide(5, colors.PRIMARY)),
                                            padding=padding.only(top=VERTICAL_PAD, left=HORIZONTAL_PAD,
                                                                 right=HORIZONTAL_PAD, bottom=VERTICAL_PAD),
                                            content=Column(
                                                spacing=COLUMN_SPACING,
                                                controls=[
                                                    Container(Text('ENDEREÇO', font_family='nunito2',
                                                                   color=colors.PRIMARY),
                                                              padding=padding.only(bottom=10)),
                                                    Row(spacing=ROW_DEFAULT_SPACING,
                                                        controls=[
                                                            Row(controls=[self.txt_cep.get, self.btn_search_cep.get],
                                                                spacing=1),
                                                            self.txt_street.get, self.txt_number.get
                                                        ]),

                                                    Row(spacing=ROW_DEFAULT_SPACING,
                                                        controls=[
                                                            self.txt_neighborhood.get,
                                                            self.txt_city.get,
                                                            self.dd_state.get,
                                                            self.txt_country.get
                                                        ]),

                                                    Row([self.txt_complement.get])
                                                ]
                                            )
                                        ),

                                        Container(height=ROW_DIVIDER_WIDTH),
                                        Container(
                                            border=border.only(left=BorderSide(5, colors.PRIMARY)),
                                            padding=padding.only(top=VERTICAL_PAD, left=HORIZONTAL_PAD,
                                                                 right=HORIZONTAL_PAD, bottom=VERTICAL_PAD),
                                            content=Column(
                                                spacing=COLUMN_SPACING,
                                                controls=[
                                                    Container(Text('ANOTAÇÕES E COMENTÁRIOS', font_family='nunito2',
                                                                   color=colors.PRIMARY),
                                                              padding=padding.only(bottom=10)),
                                                    Row([self.txt_comments.get]),
                                                    Row([self.txt_created_by.get])
                                                ]
                                            )
                                        ),

                                    ]
                                ),

                                Container(width=20),

                                Column(  # credentials column
                                    spacing=COLUMN_SPACING,
                                    controls=[
                                        Container(
                                            border=border.only(left=BorderSide(5, colors.PRIMARY)),
                                            padding=padding.only(top=VERTICAL_PAD, left=HORIZONTAL_PAD,
                                                                 right=HORIZONTAL_PAD, bottom=VERTICAL_PAD),
                                            content=Column(
                                                spacing=COLUMN_SPACING,
                                                controls=[
                                                    Container(Text('CREDENCIAIS E ACESSO', font_family='nunito2',
                                                                   color=colors.PRIMARY),
                                                              padding=padding.only(bottom=10)),
                                                    Container(height=ROW_DIVIDER_WIDTH),
                                                    self.txt_login.get, self.txt_password.get,
                                                    self.txt_confirm_password.get,
                                                    Container(height=ROW_DIVIDER_WIDTH)
                                                ]
                                            )
                                        ),
                                        Container(height=ROW_DIVIDER_WIDTH + 20),
                                        Container(
                                            border=border.only(left=BorderSide(5, colors.PRIMARY)),
                                            padding=padding.only(top=VERTICAL_PAD, left=HORIZONTAL_PAD,
                                                                 right=HORIZONTAL_PAD, bottom=VERTICAL_PAD),

                                            content=self.specific_data_column
                                        ),
                                    ]
                                )

                            ]
                        ),

                        Container(width=ROW_DIVIDER_WIDTH),
                        Row(  # ACTION ROW
                            controls=[
                                Container(width=20),
                                self.btn_create_user.get
                            ]
                        )
                    ]
                )
            ]
        )
        return v
