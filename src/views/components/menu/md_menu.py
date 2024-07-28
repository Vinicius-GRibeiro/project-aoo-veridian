# -*- coding: utf-8 -*-

from flet import *


class Menu:
    def __init__(self, page: Page, selected_item=None):
        self.page = page
        self.selected_item = selected_item

        self.get = self._get()

    def _get(self):
        def menu_item(value, route=None, icon=None, content=None):
            # 292f3a
            bottom_color = colors.PRIMARY if self.selected_item == value else 'transparent'

            return Container(
                border=Border(None, None, BorderSide(color=bottom_color, width=1), None),
                content=MenuItemButton(
                    expand=True,
                    style=ButtonStyle(
                        overlay_color='transparent',
                        color={
                            ControlState.DEFAULT: 'white',
                            ControlState.HOVERED: colors.PRIMARY,
                        },
                    ),
                    content=Text(value=value),
                    leading=Icon(icon) if icon is not None else None,
                    on_click=lambda e: self.page.go(route) if route is not None else None
                ) if content is None else content,
                padding=padding.symmetric(vertical=10, horizontal=5),
                on_click=lambda e: self.page.go(route) if route is not None else None
            )

        mb = MenuBar(
            expand=True,
            controls=[
                menu_item(value='Início', route='/home'),

                menu_item(
                    value='Agendamentos',
                    route=None,
                    content=SubmenuButton(  # AGENDAMENTO
                        style=ButtonStyle(
                            overlay_color='transparent',
                            color={
                                ControlState.DEFAULT: 'white',
                                ControlState.HOVERED: colors.PRIMARY,
                            },
                        ),
                        menu_style=MenuStyle(
                            bgcolor='#22242A',
                            alignment=alignment.center_left,
                        ),
                        content=Container(Text("Agendamentos")),
                        controls=[
                            menu_item(value='Criar agendamento', route='/criar_agendamento', icon=icons.BOOKMARK_ADD_ROUNDED),
                            menu_item(value='Consultar agendamento', route='/consultar_agendamento', icon=icons.BOOKMARKS_ROUNDED),
                        ],
                    )
                ),

                menu_item(
                    value='Usuários',
                    route=None,
                    content=SubmenuButton(  # SUB CONTA
                        style=ButtonStyle(
                            overlay_color='transparent',
                            color={
                                ControlState.DEFAULT: 'white',
                                ControlState.HOVERED: colors.PRIMARY,
                            },
                        ),
                        menu_style=MenuStyle(
                            bgcolor='#22242A',
                            alignment=alignment.center_left,
                        ),
                        content=Container(Text("Usuários")),
                        controls=[
                            menu_item(value='Gerais', route='/geral_usuarios', icon=icons.PERSON_ROUNDED),
                            menu_item(value='Novo usuário', route='/criar_usuarios', icon=icons.ADD_ROUNDED),
                        ],
                    )
                ),

                menu_item(
                    value='Conta',
                    route=None,
                    content=SubmenuButton(  # SUB CONTA
                        style=ButtonStyle(
                            overlay_color='transparent',
                            color={
                                ControlState.DEFAULT: 'white',
                                ControlState.HOVERED: colors.PRIMARY,
                            },
                        ),
                        menu_style=MenuStyle(
                            bgcolor='#22242A',
                            alignment=alignment.center_left,
                        ),
                        content=Container(Text("Conta")),
                        controls=[
                            menu_item(value='Informações', route=None, icon=icons.INFO_OUTLINE),
                            menu_item(value='Alterar senha', route=None, icon=icons.LOCK_OPEN_OUTLINED),
                            menu_item(value='Sair', route=None, icon=icons.LOGOUT_OUTLINED),
                        ],
                    )
                )

            ]
        )

        return mb
