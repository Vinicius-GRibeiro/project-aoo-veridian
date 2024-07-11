# -*- coding: utf-8 -*-
from flet import *


def notify(page: Page, message: str, icon=None):
    sb = SnackBar(
        bgcolor='#313741',
        content=Row([
            Icon(name=icon if icon is not None else None, size=30, color=colors.PRIMARY),
            Text(value=message, font_family='nunito', color='white', size=15)
        ]),
        dismiss_direction=DismissDirection.HORIZONTAL,
        show_close_icon=True,
        close_icon_color=colors.PRIMARY,
        shape=StadiumBorder(),
        behavior=SnackBarBehavior.FLOATING,
        width=700,
    )
    page.show_snack_bar(sb)
