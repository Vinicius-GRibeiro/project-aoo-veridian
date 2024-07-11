# -*- coding: utf-8 -*-
from flet import *
from ..components.menu.md_menu import Menu
from .vw_md_usuarios import UsersTable, Txt, Choose, RefreshButton, SearchButton


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
        self.txt_status = Txt(self.page, label='Status', width=190)

        self.txt_fullname = Txt(self.page, label='Nome', width=460)

        self.txt_birthdate = Txt(self.page, label='Data nasc.', width=120)
        self.dd_gender = Choose(self.page, options=['Masculino', 'Feminino', 'Outros', '-'], selected_value=None, width=120, label='Gênero')
        self.txt_email = Txt(self.page, label='E-mail', width=210)

        self.txt_phone_1 = Txt(self.page, label='Cel.', width=227)
        self.txt_phone_2 = Txt(self.page, label='Cel. 2', width=227)

        self.txt_zip_code = Txt(self.page, label='CEP', width=120)
        self.txt_street = Txt(self.page, label='Rua', width=335)

        self.txt_number = Txt(self.page, label='Nº', width=100)
        self.txt_neighborhood= Txt(self.page, label='Bairro', width=355)

        self.txt_city = Txt(self.page, label='Cidade', width=250)
        self.dd_state = Choose(self.page, label='UF', width=80, options=[])
        self.txt_country = Txt(self.page, label='País', width=120)

        self.txt_complement = Txt(self.page, label='Complemento', width=460)

        self.txt_comments = Txt(self.page, label='Comentários', width=460)

        self.txt_type = Txt(self.page, label='Tipo', width=150)
        self.txt_created_by = Txt(self.page, label='Criado por', width=305, read_only=True)

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

        self.users_table = UsersTable(self.page, controls=[
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
            self.txt_created_by
        ])

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
        self.menu_footer = Menu(self.page, selected_item='Usuários').get
        self.get_view = self._get_view()

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
                                    shadow=BoxShadow(spread_radius=2, blur_radius=10, color='black', offset=Offset(x=0, y=15)),
                                    border=Border(top=None, right=None, bottom=None, left=BorderSide(5, self.page.session.get('bg_main_color_dark'))),
                                    content=Row(
                                        controls=[
                                            Container(width=50, height=10),
                                            Column(
                                                controls=[
                                                    Container(height=40),
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
                                                                            controls=[self.txt_fullname.get]),
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
                                                                            controls=[self.txt_complement.get]),
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
                                                                            controls=[self.txt_comments.get]),
                                                                        Row(spacing=6, controls=[
                                                                            self.txt_type.get,
                                                                            self.txt_created_by.get
                                                                        ])
                                                                    ]
                                                                )
                                                            ]
                                                        )
                                                    )
                                                ]
                                            ),
                                            Container(width=20, height=10),
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
