# -*- coding: utf-8 -*-
from flet import *
from src.views.components.menu.md_menu import Menu
from .vw_md_agendamentos_novo import (PatientsTable, Txt, SearchButton, RefreshButton, Choose, DoctorsTable,
                                      DoctorAvalTable, SimpleTextButton)

VERTICAL_PAD = 5
HORIZONTAL_PAD = 20
ROW_DIVIDER_WIDTH = 15
COLUMN_SPACING = 7


class ViewAgendamentoNovo:
    def __init__(self, page: Page):
        self.page = page

        self.txt_filter_by_name = Txt(self.page, hint='Buscar por nome', width=400)
        self.txt_filter_by_cpf = Txt(self.page, hint='Buscar por CPF', width=280)
        self.users_table = PatientsTable(self.page)

        self.btn_search_user = SearchButton(self.page, icon=icons.SEARCH_ROUNDED, controls=[self.users_table,
                                                                                            self.txt_filter_by_name,
                                                                                            self.txt_filter_by_cpf])

        self.btn_refresh_filters_patients = RefreshButton(self.page, icon=icons.REFRESH_ROUNDED, user_type='paciente',
                                                          controls=[self.users_table,
                                                                    self.txt_filter_by_name,
                                                                    self.txt_filter_by_cpf])

        self.dd_doctor_specialty = Choose(self.page, label='Especialidade', options=
        ['angiologista', 'cardiologista', 'dentista', 'dermatologista',
         'endocrinologista', 'fonoaudiólogo', 'geriatra', 'ginecologista',
         'hematologista', 'nefrologista',
         'neurologista', 'nutricionista', 'obstetricista', 'oftalmologista',
         'oncologista', 'ortopedista',
         'otorrinolaringologista', 'pediatra', 'psicólogo', 'pneumologista',
         'proctologista', 'psiquiatra', 'reumatologista',
         'urologista'])
        self.dd_doctor_specialty.get.on_change = lambda e: self.__on_specialty_change(e)

        self.doc_aval_table = DoctorAvalTable(self.page)
        self.doctors_table = DoctorsTable(self.page, self.doc_aval_table)

        self.btn_refresh_filters_doctors = RefreshButton(self.page, icon=icons.REFRESH_ROUNDED, user_type='médico',
                                                         controls=[self.doctors_table])

        self.btn_create_appointment = SimpleTextButton(self.page, text='+ Criar consulta', controls=[
            self.users_table, self.doctors_table, self.doc_aval_table
        ])

        self.get_view = self._get_view()

    def __on_specialty_change(self, e: ControlEvent):
        if e.data == '' and e.data is None:
            return

        self.doctors_table.populate_table(conditions=f"specialty = '{e.data}'", reverse=True)

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
                        Row(controls=[Menu(self.page, selected_item='Agendamentos').get]),  # Menu row
                        Container(height=20),
                        Row(  # Content row
                            alignment=MainAxisAlignment.CENTER,
                            spacing=0,
                            controls=[
                                Container(width=5),

                                Container(  # Patient table container
                                    border=border.only(left=BorderSide(1, 'transparent')),
                                    padding=padding.only(top=VERTICAL_PAD, left=HORIZONTAL_PAD,
                                                         right=HORIZONTAL_PAD, bottom=VERTICAL_PAD - 10),
                                    content=Column(  # Patient Table column
                                        spacing=5,
                                        controls=[
                                            Container(Text('PACIENTE', font_family='nunito2',
                                                           color=colors.PRIMARY)),
                                            Container(height=5),
                                            Row(
                                                spacing=15,
                                                controls=[
                                                    Container(content=self.txt_filter_by_name.get),
                                                ]
                                            ),

                                            Row(
                                                spacing=15,
                                                controls=[
                                                    Container(content=self.txt_filter_by_cpf.get),
                                                    self.btn_search_user.get, self.btn_refresh_filters_patients.get
                                                ]
                                            ),

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
                                ),

                                Container(  # Doctor table container
                                    border=border.only(left=BorderSide(1, 'transparent')),
                                    padding=padding.only(top=VERTICAL_PAD, left=HORIZONTAL_PAD,
                                                         right=HORIZONTAL_PAD, bottom=VERTICAL_PAD - 10),
                                    content=Column(  # Doctor Table column
                                        spacing=5,
                                        controls=[
                                            Container(Text('MÉDICO', font_family='nunito2',
                                                           color=colors.PRIMARY)),
                                            Container(height=5),
                                            Row(
                                                spacing=15,
                                                controls=[
                                                    self.dd_doctor_specialty.get,
                                                    self.btn_refresh_filters_doctors.get,
                                                ]
                                            ),
                                            Container(height=35),
                                            Container(
                                                content=Column(
                                                    controls=[
                                                        Container(self.doctors_table.get)
                                                    ],
                                                    scroll=ScrollMode.HIDDEN, height=450
                                                ),

                                                bgcolor=self.page.session.get('bg_main_color_dark'),
                                                border_radius=25,
                                                clip_behavior=ClipBehavior.ANTI_ALIAS
                                            )
                                        ],
                                    ),
                                ),

                                Container(  # Availability table container
                                    border=border.only(left=BorderSide(1, 'transparent')),
                                    padding=padding.only(top=VERTICAL_PAD, left=HORIZONTAL_PAD,
                                                         right=HORIZONTAL_PAD, bottom=VERTICAL_PAD - 10),
                                    content=Column(  # Doctor Table column
                                        spacing=5,
                                        controls=[
                                            Container(Text('DATA E HORA', font_family='nunito2',
                                                           color=colors.PRIMARY)),
                                            Container(height=80),
                                            Container(
                                                content=Column(
                                                    controls=[
                                                        Container(self.doc_aval_table.get)
                                                    ],
                                                    scroll=ScrollMode.HIDDEN, height=450
                                                ),

                                                bgcolor=self.page.session.get('bg_main_color_dark'),
                                                border_radius=25,
                                                clip_behavior=ClipBehavior.ANTI_ALIAS
                                            )
                                        ],
                                    ),
                                )

                            ]
                        ),

                        Row(
                            alignment=MainAxisAlignment.END,
                            controls=[
                                Container(self.btn_create_appointment.get, padding=padding.only(top=10)),
                                Container(width=60)
                            ]
                        )
                    ]
                )
            ]
        )
        return v
