# -*- coding: utf-8 -*-
from flet import *
from src.views.components.menu.md_menu import Menu
from .vw_md_agendamentos_consultar import AppointmentsTable, Txt, Choose


class ViewAgendamentoConsultar:
    def __init__(self, page: Page):
        self.page = page

        self.appointments_table = AppointmentsTable(self.page)

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
                        Row(controls=[Menu(self.page, selected_item='Agendamentos').get]),  # Menu row
                        Container(height=20),
                        Row(  # content row
                            spacing=0,
                            alignment=MainAxisAlignment.CENTER,
                            controls=[
                                Container(
                                    content=Column(
                                        controls=[
                                            Container(self.appointments_table.get)
                                        ],
                                        scroll=ScrollMode.HIDDEN, height=500
                                    ),

                                    bgcolor=self.page.session.get('bg_main_color_dark'),
                                    border_radius=25,
                                    clip_behavior=ClipBehavior.ANTI_ALIAS
                                )
                            ]
                        )
                    ]
                )
            ]
        )

        return v
