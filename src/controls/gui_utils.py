# -*- coding: utf-8 -*-
from flet import *
from src.models.md_users import User


def notify(page: Page, message: str, icon=None):
    sb = SnackBar(
        bgcolor=colors.PRIMARY,
        content=Row([
            Icon(name=icon if icon is not None else None, size=30, color=colors.ON_PRIMARY),
            Text(value=message, font_family='nunito2', color=colors.ON_PRIMARY, size=15)
        ]),
        dismiss_direction=DismissDirection.HORIZONTAL,
        show_close_icon=True,
        close_icon_color=colors.ON_PRIMARY,
        shape=StadiumBorder(),
        behavior=SnackBarBehavior.FLOATING,
        margin=80,
    )
    page.show_snack_bar(sb)


def modal(page: Page, title: str, description: str):
    ad = AlertDialog(
        title=Text(value=title, font_family='nunito'),
        content=Text(value=description, font_family='nunito'),
        actions=[
            TextButton(text='Confirmar', on_click=lambda e: None),
            TextButton(text='Cancelar', on_click=lambda e: None),
        ],
        actions_alignment=MainAxisAlignment.END
    )

    page.open(ad)
