# -*- coding: utf-8 -*-
from flet import ThemeMode
import flet_easy as fs
from src.views.vw_login.vw_login import ViewLogin
from src.views.vw_home.vw_home import ViewHome
from src.views.vw_usuarios.vw_usuarios import ViewUsuarios
from src.views.vw_usuarios_novos.vw_usuarios_novos import ViewUsuariosNovos
from src.views.vw_agendamentos_novo.vw_agendamentos_novo import ViewAgendamentoNovo
from src.views.vw_agendamentos_consultar.vw_agendamentos_consultar import ViewAgendamentoConsultar
from assets import fonts

app = fs.FletEasy(route_init='/consultar_agendamento')


@app.page(route='/login', title='Login')
def login_page(data: fs.Datasy):
    page = data.page

    page.theme_mode = ThemeMode.DARK
    page.session.set('logged_user_id', '')
    page.session.set('logged_user_type', '')

    page.session.set('bg_main_color_light', '#323741')
    page.session.set('bg_main_color_dark', '#22242a')

    data.page.window_maximized = True
    data.page.window_maximizable = False
    data.page.window_resizable = False

    page.fonts = fonts.fonts
    page.spacing = 0
    page.padding = 0

    return ViewLogin(page).get_view


@app.page(route='/home', title='Home')
def home_page(data: fs.Datasy):
    # REMOVER EM PRODUÇÃO
    data.page.fonts = fonts.fonts
    data.page.spacing = 0
    data.page.padding = 0
    data.page.session.set('bg_main_color_light', '#323741')
    data.page.session.set('bg_main_color_dark', '#22242a')
    data.page.window_maximized = True
    data.page.window_maximizable = False
    data.page.window_resizable = False

    return ViewHome(data.page).get_view


@app.page(route='/geral_usuarios', title='Usuários')
def users_page(data: fs.Datasy):
    # REMOVER EM PRODUÇÃO
    data.page.fonts = fonts.fonts
    data.page.spacing = 0
    data.page.padding = 0
    data.page.session.set('bg_main_color_light', '#323741')
    data.page.session.set('bg_main_color_dark', '#22242a')
    data.page.window_maximized = True
    data.page.window_maximizable = False
    data.page.window_resizable = False

    return ViewUsuarios(data.page).get_view


@app.page(route='/criar_usuarios', title='Criar usuário')
def users_page(data: fs.Datasy):
    # REMOVER EM PRODUÇÃO
    data.page.fonts = fonts.fonts
    data.page.spacing = 0
    data.page.padding = 0
    data.page.session.set('bg_main_color_light', '#323741')
    data.page.session.set('bg_main_color_dark', '#22242a')
    data.page.window_maximized = True
    data.page.window_maximizable = False
    data.page.window_resizable = False

    data.page.session.set('logged_user_id', 25)
    data.page.session.set('logged_user_type', 'paciente')

    return ViewUsuariosNovos(data.page).get_view


@app.page(route='/criar_agendamento', title='Novo agendamento')
def users_page(data: fs.Datasy):
    # REMOVER EM PRODUÇÃO
    data.page.fonts = fonts.fonts
    data.page.spacing = 0
    data.page.padding = 0
    data.page.session.set('bg_main_color_light', '#323741')
    data.page.session.set('bg_main_color_dark', '#22242a')
    data.page.window_maximized = True
    data.page.window_maximizable = False
    data.page.window_resizable = False

    data.page.session.set('logged_user_id', 25)
    data.page.session.set('logged_user_type', 'paciente')

    return ViewAgendamentoNovo(data.page).get_view


@app.page(route='/consultar_agendamento', title='Consultar agendamentos')
def read_appointments_page(data: fs.Datasy):
    # REMOVER EM PRODUÇÃO
    data.page.fonts = fonts.fonts
    data.page.spacing = 0
    data.page.padding = 0
    data.page.session.set('bg_main_color_light', '#323741')
    data.page.session.set('bg_main_color_dark', '#22242a')
    data.page.window_maximized = True
    data.page.window_maximizable = False
    data.page.window_resizable = False

    data.page.session.set('logged_user_id', 25)
    data.page.session.set('logged_user_type', 'paciente')

    return ViewAgendamentoConsultar(data.page).get_view


app.run()
