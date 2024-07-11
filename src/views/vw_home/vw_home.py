# -*- coding: utf-8 -*-
from flet import *
from ..components.menu.md_menu import Menu


class ViewHome:
    def __init__(self, page: Page):
        self.page = page

        ...

        self.get_view = self._get_view()

    def _get_view(self) -> View:
        v = View(
            spacing=0,
            padding=0,
            bgcolor=self.page.session.get('bg_main_color_light'),
            controls=[
                Column(
                    controls=[
                        Row(controls=[Menu(self.page, selected_item='Início').get]),

                    ]
                )
            ]
        )

        return v
