# -*- coding: utf-8 -*-
from flet import *
from ..components.menu.md_menu import Menu
from .vw_md_usuarios import (UsersTable, Txt, Choose, RefreshButton, SearchButton, ClearFormButton,
                             UpdateUserFormButton, DoctorAvalTable)
from src.controls.gui_utils import notify
from src.models.md_users import Patient, Doctor, Employee


class ViewUsuarios:
    def __init__(self, page: Page):
        self.page = page

        self.txt_filter_by_name = Txt(self.page, hint='Buscar por nome')
        self.txt_filter_by_cpf = Txt(self.page, hint='Buscar por CPF')
        self.dd_filter_by_type = Choose(self.page, hint='tipo de usuário',
                                        options=['todos', 'funcionário', 'médico', 'paciente'])

        # DEFAULT SPACING FOR ROWS = 5
        # TOTAL ROW WIDTH = 460
        self.txt_id = Txt(self.page, read_only=True, label='ID', width=60)
        self.txt_cpf = Txt(self.page, label='CPF', width=200)
        self.txt_status = Txt(self.page, label='Status', width=190, read_only=True)

        self.txt_fullname = Txt(self.page, label='Nome', width=460)

        self.txt_birthdate = Txt(self.page, label='Data nasc.', width=120)
        self.dd_gender = Choose(self.page, options=['Masculino', 'Feminino', 'Outros', '-'], selected_value=None,
                                width=120, label='Gênero')
        self.txt_email = Txt(self.page, label='E-mail', width=210)

        self.txt_phone_1 = Txt(self.page, label='Cel.', width=227)
        self.txt_phone_2 = Txt(self.page, label='Cel. 2', width=227)

        self.txt_zip_code = Txt(self.page, label='CEP', width=120)
        self.txt_street = Txt(self.page, label='Rua', width=335)

        self.txt_number = Txt(self.page, label='Nº', width=100)
        self.txt_neighborhood = Txt(self.page, label='Bairro', width=355)

        self.txt_city = Txt(self.page, label='Cidade', width=250)
        self.dd_state = Choose(self.page, label='UF', width=80, options=["AC", "AL", "AP", "AM", "BA", "CE", "DF",
                                                                         "ES", "GO", "MA", "MT", "MS",
                                                                         "MG", "PA", "PB", "PR", "PE", "PI", "RJ",
                                                                         "RN", "RS", "RO", "RR", "SC",
                                                                         "SP", "SE", "TO"])
        self.txt_country = Txt(self.page, label='País', width=120)

        self.txt_complement = Txt(self.page, label='Complemento', width=460)

        self.txt_comments = Txt(self.page, label='Comentários', width=460)

        self.txt_type = Choose(self.page, label='Tipo', width=150, options=['funcionário', 'médico', 'paciente'])
        self.txt_created_by = Txt(self.page, label='Criado por', width=305, read_only=True)

        self.ctrlpacient_insurance = Txt(self.page, label='Seguro ou convênio', width=400)

        self.ctrlemployee_role = Txt(self.page, label='Cargo', width=400)

        self.ctrldoctor_crm = Txt(self.page, label='CRM', width=400)
        self.ctrldoctor_specialty = Choose(self.page, label='Especialidade',
                                           options=['angiologista', 'cardiologista', 'dentista', 'dermatologista',
                                                    'endocrinologista', 'fonoaudiólogo', 'geriatra', 'ginecologista',
                                                    'hematologista', 'nefrologista',
                                                    'neurologista', 'nutricionista', 'obstetricista', 'oftalmologista',
                                                    'oncologista', 'ortopedista',
                                                    'otorrinolaringologista', 'pediatra', 'psicólogo', 'pneumologista',
                                                    'proctologista', 'psiquiatra', 'reumatologista',
                                                    'urologista'], width=400)
        self.ctrldoctor_price = Txt(self.page, label='Preço da consulta (R$)', width=400)

        self.rg_filter_by_status = RadioGroup(
            value='todos',
            content=Row(
                controls=[
                    Radio(label='todos', value='todos'),
                    Radio(label='regulares', value='regulares', active_color='green'),
                    Radio(label='bloqueados', value='bloqueados', active_color='red'),
                ]
            )
        )

        self.form_controls_list = [
            self.txt_id,
            self.txt_cpf,
            self.txt_status,
            self.txt_fullname,
            self.txt_birthdate,
            self.dd_gender,
            self.txt_email,
            self.txt_phone_1,
            self.txt_phone_2,
            self.txt_zip_code,
            self.txt_street,
            self.txt_number,
            self.txt_neighborhood,
            self.txt_city,
            self.dd_state,
            self.txt_country,
            self.txt_complement,
            self.txt_comments,
            self.txt_type,
            self.txt_created_by,
            self.ctrlpacient_insurance,
            self.ctrlemployee_role,
            self.ctrldoctor_crm,
            self.ctrldoctor_specialty,
            self.ctrldoctor_price
        ]

        self.ctrldoctor_avals = DoctorAvalTable(self.page, self.form_controls_list)

        self.users_table = UsersTable(self.page, controls=self.form_controls_list)

        self.btn_refresh = RefreshButton(self.page, icons.REFRESH_ROUNDED, controls=[self.users_table,
                                                                                     self.txt_filter_by_name,
                                                                                     self.txt_filter_by_cpf,
                                                                                     self.dd_filter_by_type,
                                                                                     self.rg_filter_by_status])
        self.btn_search = SearchButton(self.page, icons.SEARCH_ROUNDED, controls=[self.users_table,
                                                                                  self.txt_filter_by_name,
                                                                                  self.txt_filter_by_cpf,
                                                                                  self.dd_filter_by_type,
                                                                                  self.rg_filter_by_status])

        self.btn_clear_form = ClearFormButton(self.page, icon=icons.CLEANING_SERVICES_ROUNDED,
                                              controls=self.form_controls_list, color=colors.YELLOW)
        self.btn_update_user = UpdateUserFormButton(self.page, icon=icons.DONE_ROUNDED,
                                                    controls=self.form_controls_list)

        self.secondary_tab = Tab(text='Dados específicos', content=Column(
            controls=[],
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER
        ))

        self.main_tab = Tabs(
            on_change=lambda e: self.on_tab_change(e),
            selected_index=0,
            height=580,
            tabs=[
                Tab(
                    text='Dados gerais',
                    content=Row(
                        controls=[
                            Container(width=50, height=5),
                            Column(
                                controls=[
                                    Container(height=20),
                                    Container(
                                        border=Border(top=None, right=None, bottom=None,
                                                      left=BorderSide(1, colors.PRIMARY)),
                                        content=Row(
                                            controls=[
                                                Container(width=20),
                                                Column(
                                                    controls=[
                                                        Row(spacing=5, controls=[
                                                            self.txt_id.get,
                                                            self.txt_cpf.get,
                                                            self.txt_status.get
                                                        ]),
                                                        Row(spacing=5,
                                                            controls=[
                                                                self.txt_fullname.get]),
                                                        Row(spacing=5, controls=[
                                                            self.txt_birthdate.get,
                                                            self.dd_gender.get,
                                                            self.txt_email.get
                                                        ]),
                                                        Row(spacing=6, controls=[
                                                            self.txt_phone_1.get,
                                                            self.txt_phone_2.get,
                                                        ])
                                                    ]
                                                )
                                            ]
                                        )
                                    ),

                                    Container(height=15),

                                    Container(
                                        border=Border(top=None, right=None, bottom=None,
                                                      left=BorderSide(1, colors.PRIMARY)),
                                        content=Row(
                                            controls=[
                                                Container(width=20),
                                                Column(
                                                    controls=[
                                                        Row(spacing=5, controls=[
                                                            self.txt_zip_code.get,
                                                            self.txt_street.get
                                                        ]),
                                                        Row(spacing=5, controls=[
                                                            self.txt_number.get,
                                                            self.txt_neighborhood.get
                                                        ]),
                                                        Row(spacing=5, controls=[
                                                            self.txt_city.get,
                                                            self.dd_state.get,
                                                            self.txt_country.get
                                                        ]),
                                                        Row(spacing=5,
                                                            controls=[
                                                                self.txt_complement.get]),
                                                    ]
                                                )
                                            ]
                                        )
                                    ),

                                    Container(height=15),

                                    Container(
                                        border=Border(top=None, right=None, bottom=None,
                                                      left=BorderSide(1, colors.PRIMARY)),
                                        content=Row(
                                            controls=[
                                                Container(width=20),
                                                Column(
                                                    controls=[
                                                        Row(spacing=5,
                                                            controls=[
                                                                self.txt_comments.get]),
                                                        Row(spacing=6, controls=[
                                                            self.txt_type.get,
                                                            self.txt_created_by.get
                                                        ])
                                                    ]
                                                )
                                            ]
                                        )
                                    ),
                                    Container(height=5),

                                ]
                            ),
                            Container(width=20, height=10),
                        ]
                    )
                ),

                self.secondary_tab
            ]
        )

        self.menu_footer = Menu(self.page, selected_item='Usuários').get
        self.get_view = self._get_view()

    def on_tab_change(self, e: ControlEvent):
        new_controls = []
        selected_index = self.main_tab.selected_index

        if selected_index == 1:
            match self.txt_type.get.value:
                case 'médico':
                    new_controls = [
                        self.ctrldoctor_crm.get, self.ctrldoctor_specialty.get, self.ctrldoctor_price.get,
                        self.ctrldoctor_avals.get_container
                    ]

                    if self.txt_id.get.value != '':
                        doctors_data = Doctor(self.page).read_doctor(user_id=self.txt_id.get.value)[0]
                        crm, specialty = doctors_data[1], doctors_data[2]
                        price = float(doctors_data[3].replace(',', '.').replace('R$ ', ''))

                        self.ctrldoctor_crm.get.value = crm
                        self.ctrldoctor_specialty.get.value = specialty
                        self.ctrldoctor_price.get.value = price
                        self.ctrldoctor_avals.populate_table()

                case 'funcionário':
                    new_controls = [self.ctrlemployee_role.get]

                    if self.txt_id.get.value != '':
                        employee_role = Employee(self.page).read_employee(user_id=self.txt_id.get.value, columns='role')[0][
                            0]
                        self.ctrlemployee_role.get.value = employee_role
                case 'paciente':
                    new_controls = [self.ctrlpacient_insurance.get]

                    if self.txt_id.get.value != '':
                        patient_insurance = \
                            Patient(self.page).read_patient(user_id=self.txt_id.get.value, columns='insurance')[0][0]
                        self.ctrlpacient_insurance.get.value = patient_insurance
                case 'todos':
                    notify(self.page, 'Selecione um tipo de usuário para ter acesso aos dados específicos',
                           icons.NEW_RELEASES_ROUNDED)

        self.secondary_tab.content.controls.clear()
        for new_control in new_controls:
            self.secondary_tab.content.controls.append(new_control)

        self.page.update()

    def _get_view(self) -> View:
        v = View(
            spacing=0,
            padding=0,
            bgcolor=self.page.session.get('bg_main_color_light'),
            controls=[
                Column(
                    spacing=0,
                    controls=[
                        Row(controls=[Menu(self.page, selected_item='Usuários').get]),  # Menu row
                        Row(  # Content row
                            spacing=0,
                            controls=[
                                Container(width=15),
                                Column(  # Table column
                                    spacing=10,
                                    controls=[
                                        Container(height=15),
                                        Row(
                                            spacing=15,
                                            controls=[
                                                Container(content=self.txt_filter_by_name.get,
                                                          ),
                                                Container(content=self.txt_filter_by_cpf.get,
                                                          ),
                                            ]
                                        ),

                                        Row(
                                            width=680,
                                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                                            controls=[
                                                Container(content=self.dd_filter_by_type.get),
                                                self.rg_filter_by_status,
                                                Container(
                                                    content=Row(
                                                        controls=[
                                                            self.btn_refresh.get,
                                                            self.btn_search.get
                                                        ]
                                                    )
                                                )
                                            ]
                                        ),

                                        Container(height=20),

                                        Container(
                                            content=Column(
                                                controls=[
                                                    Container(self.users_table.get)
                                                ],
                                                scroll=ScrollMode.HIDDEN, height=450
                                            ),

                                            bgcolor=self.page.session.get('bg_main_color_dark'),
                                            border_radius=25,
                                            clip_behavior=ClipBehavior.ANTI_ALIAS
                                        )
                                    ],
                                ),

                                Container(width=15),

                                Container(
                                    expand=True,
                                    bgcolor=self.page.session.get('bg_main_color_dark'),
                                    height=650,
                                    shadow=BoxShadow(spread_radius=2, blur_radius=10, color='black',
                                                     offset=Offset(x=0, y=15)),
                                    border=Border(top=None, right=None, bottom=None,
                                                  left=BorderSide(5, self.page.session.get('bg_main_color_dark'))),
                                    content=Column(
                                        controls=[
                                            self.main_tab,

                                            Container(
                                                padding=padding.only(right=100, bottom=10),
                                                content=Row(
                                                    alignment=MainAxisAlignment.END,
                                                    controls=[
                                                        self.btn_clear_form.get,
                                                        self.btn_update_user.get,
                                                    ]
                                                ),
                                            )

                                        ]
                                    )
                                ),
                            ]
                        ),

                    ]
                )
            ]
        )
        return v
