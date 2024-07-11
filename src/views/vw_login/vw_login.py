# -*- coding: utf-8 -*-
from flet import *
from .vw_md_login import Btn, BtnText
from fletmint import TextInput


class ViewLogin:
    def __init__(self, page: Page):
        self.txt_email = TextInput(width=500, prefix=Icon(icons.EMAIL_ROUNDED))
        self.txt_senha = TextInput(width=500, password=True, prefix=Icon(icons.PASSWORD_ROUNDED))
        self.btn_login = Btn(text='Entrar', page=page, email_input=self.txt_email, password_input=self.txt_senha)
        self.btn_esqueci_a_senha = BtnText('esqueci a senha')

        self.get_view = self._get_view()

    def _get_view(self) -> View:
        shadow_veridian_logo = BoxShadow(spread_radius=.5,
                                         blur_radius=1,
                                         color='white')

        v = View(
            bgcolor='#22242A',
            controls=[
                Row(
                    expand=True,
                    controls=[
                        Container(
                            shadow=BoxShadow(spread_radius=3, blur_radius=50, color='#292f3a',
                                             blur_style=ShadowBlurStyle.OUTER),
                            content=Container(
                                content=Column([
                                    Icon(name=icons.PERSON_PIN_ROUNDED, size=100),
                                    Container(height=25),
                                    self.txt_email,
                                    self.txt_senha,
                                    Container(self.btn_esqueci_a_senha.get, alignment=alignment.center_right,
                                              width=550),
                                    Container(height=25),
                                    self.btn_login.get,
                                ], alignment=MainAxisAlignment.CENTER, horizontal_alignment=CrossAxisAlignment.CENTER))
                        ),
                        Container(expand=True,
                                  content=Column([
                                      Container(Text(value='VERIDIAN', font_family='nunito',
                                                     color=colors.PRIMARY, size=50, weight=FontWeight.BOLD
                                                     ), padding=padding.symmetric(10, 50)),
                                      Container(height=5, width=90, bgcolor=colors.PRIMARY,
                                                shadow=shadow_veridian_logo),
                                      Container(height=5, width=60, bgcolor=colors.PRIMARY,
                                                shadow=shadow_veridian_logo),
                                      Container(height=5, width=30, bgcolor=colors.PRIMARY, shadow=shadow_veridian_logo)
                                  ],
                                      alignment=MainAxisAlignment.CENTER,
                                      horizontal_alignment=CrossAxisAlignment.CENTER),
                                  alignment=alignment.center)
                    ]
                )
            ]
        )
        return v

# 22242A mais cinzinha
# 292f3a borda
