# -*- coding: utf-8 -*-
from flet import *
from src.models.md_appointments import Appointment
from src.models.md_users import Doctor, User
from src.models.md_doctor_availability import DocAvailability
import datetime
from abc import ABC, abstractmethod
from src.controls.gui_utils import notify

BORDER_RADIUS = 10
BORDER_COLORS = '#494D5F'


class Txt:
    def __init__(self, page: Page, width: int = 330, scale: float = 1.0, read_only: bool = False, label: str = None,
                 hint: str = None, is_dense: bool = True, input_filter: InputFilter = None, password: bool = False):
        self.page = page
        self.hint = hint
        self.width = width
        self.scale = scale
        self.read_only = read_only
        self.label = label
        self.is_dense = is_dense
        self.input_filter = input_filter
        self.password = password
        self.get = self._get()

    def _get(self) -> TextField:
        txt = TextField(
            read_only=self.read_only,
            hint_text=self.hint if self.hint is not None else None,
            label=self.label if self.label is not None else None,
            height=35,
            cursor_width=2,
            dense=self.is_dense,
            password=self.password,
            can_reveal_password=self.password,
            input_filter=self.input_filter if self.input_filter is not None else None,
            hint_style=TextStyle(
                color='#494D5F',
                font_family='nunito2',
                size=14
            ),
            width=self.width,
            scale=self.scale,
            border_color=BORDER_COLORS,
            border_radius=BORDER_RADIUS,
            border_width=2,
            bgcolor='#22242a',
            text_style=TextStyle(
                color='#C3C3C8',
                font_family='nunito'
            ),
            label_style=TextStyle(
                color=colors.PRIMARY,
                font_family='nunito'
            ),
            on_focus=self.on_focus_state,
            on_blur=self.remove_focus_state,
        )

        return txt

    @staticmethod
    def on_focus_state(e: ControlEvent):
        e.control.border_color = '#C3C3C8'
        e.control.border_width = 1
        e.control.update()

    @staticmethod
    def remove_focus_state(e: ControlEvent):
        e.control.border_color = '#494D5F'
        e.control.border_width = 2
        e.control.update()


class Choose:
    def __init__(self, page: Page, options: list, scale: float = 1, selected_value=None, hint: str = None,
                 label: str = None, width: float = 200, is_dense: bool = True):
        self.page = page
        self.scale = scale
        self.hint = hint
        self.options = options
        self.selected_value = selected_value
        self.label = label
        self.width = width
        self.is_dense = is_dense

        self.get = self._get()

    def _get(self) -> Dropdown:
        dd = Dropdown(
            value=self.selected_value,
            width=self.width,
            scale=self.scale,
            height=38,
            dense=self.is_dense,
            bgcolor='#22242a',
            border_color=BORDER_COLORS,
            border_radius=BORDER_RADIUS,
            border_width=2,
            alignment=alignment.center,
            hint_style=TextStyle(
                color='#494D5F',
                font_family='nunito',
            ),
            hint_text=self.hint,
            text_style=TextStyle(
                font_family='nunito2',
                size=13,
                color='#C3C3C8'
            ),
            elevation=0,
            options=[],
            label=self.label,
            label_style=TextStyle(
                font_family='nunito2',
                size=13,
                color=colors.PRIMARY
            ),
        )

        for op in self.options:
            dd.options.append(dropdown.Option(op))

        return dd


class AppointmentsTable:
    def __init__(self, page: Page):
        self.page = page
        self.selected_row = None
        self.get = self._get()

        self.populate_table()

    def populate_table(self, conditions=None):
        if conditions is not None and conditions != '':
            appointments = Appointment(self.page).read_appointment(columns="appointment_id, pacient_id, doctor_id, "
                                                                           "date_aval_id, status, total_price",
                                                                   condition=conditions, order_by='appointment_id')
        else:
            appointments = Appointment(self.page).read_appointment(columns="appointment_id, pacient_id, doctor_id, "
                                                                           "date_aval_id, status, total_price",
                                                                   order_by='appointment_id')

        if appointments is None or len(appointments) <= 0:
            return

        self.get.rows.clear()

        for ap in appointments:
            ap_id = ap[0]
            pat_id = ap[1]
            doc_id = ap[2]
            aval_id = ap[3]

            doc_especialty = Doctor(self.page).read_doctor(columns='specialty', user_id=doc_id)[0][0]
            pat_cpf, pat_name = User(self.page).read_user(columns='cpf, fullname', user_id=pat_id)[0]
            aval_date, aval_hour, aval_id = \
                DocAvailability(self.page).read_availability(columns='aval_date, aval_hour, aval_id', aval_id=aval_id)[0]
            aval_date, aval_hour = aval_date.strftime('%d/%m/%Y'), aval_hour.strftime('%H:%M')

            status = ap[4]
            price = ap[5]

            self.add_new_user_line(ap_id, pat_cpf, pat_name, doc_especialty, aval_date, aval_hour, price, status, aval_id)

    def _get(self) -> DataTable:
        dt = DataTable(
            width=1200,
            column_spacing=10,
            horizontal_lines=BorderSide(width=.5, color=colors.PRIMARY),
            columns=[
                DataColumn(label=Row([Icon(name=icons.GRID_3X3_ROUNDED), Text(value='ID', font_family='nunito')])),
                DataColumn(
                    label=Row([Icon(name=icons.FEATURED_PLAY_LIST_ROUNDED), Text(value='CPF', font_family='nunito')],
                              width=110)),
                DataColumn(
                    label=Row([Icon(name=icons.PERSON_ROUNDED), Text(value='Nome', font_family='nunito')], width=150)),
                DataColumn(
                    label=Row([Icon(name=icons.LIST_ALT_ROUNDED ), Text(value='Especialidade', font_family='nunito')])),
                DataColumn(label=Row([Icon(name=icons.CALENDAR_TODAY_ROUNDED), Text(value='Data', font_family='nunito')])),
                DataColumn(label=Row([Icon(name=icons.ACCESS_TIME_ROUNDED), Text(value='Hora', font_family='nunito')])),
                DataColumn(label=Row([Icon(name=icons.ATTACH_MONEY_ROUNDED), Text(value='Preço', font_family='nunito')])),
                DataColumn(label=Row([Icon(name=icons.PERSON_ROUNDED), Text(value='Status', font_family='nunito')])),
                DataColumn(label=Row([Container(width=25), Icon(name=icons.RADIO_BUTTON_ON_ROUNDED), Text(value='Ações', font_family='nunito')])),
            ],
        )
        return dt

    def add_new_user_line(self, id_, cpf, name, specialty, date, hour, price, status, aval_id):
        self.get.rows.append(
            DataRow(cells=[
                DataCell(content=Text(value=id_, font_family='nunito')),
                DataCell(content=Text(value=cpf, font_family='nunito')),
                DataCell(content=Text(value=name, font_family='nunito')),
                DataCell(content=Text(value=specialty, font_family='nunito')),
                DataCell(content=Text(value=date, font_family='nunito')),
                DataCell(content=Text(value=hour, font_family='nunito')),
                DataCell(content=Text(value=price, font_family='nunito')),
                DataCell(content=Text(value=status, font_family='nunito')),

                DataCell(content=Row([
                    Container(width=25),
                    TableActionBtnCancel(self.page, icon=icons.DO_NOT_DISTURB_OFF, ap_id=id_, aval_id=aval_id,
                                         color=colors.RED, table=self,
                                         diseabled_=True if status == 'cancelado' or status == 'concluído' else False).get,
                    TableActionBtnDone(self.page, icon=icons.DONE_ROUNDED, ap_id=id_, aval_id=aval_id, table=self,
                                       diseabled_=True if status == 'cancelado' or status == 'concluído' else False).get
                ])),

            ], on_select_changed=lambda e: self.__on_row_selected(e),
            )
        )

    def __on_row_selected(self, e: ControlEvent):
        ...


class SimpleIconButton(ABC):
    def __init__(self, page: Page, icon: str, controls: list, color: str = colors.PRIMARY):
        self.page = page

        self.icon = icon
        self.controls = controls
        self.color = color

        self.get = self._get()

    def _get(self) -> IconButton:
        ic = IconButton(
            icon=self.icon,
            icon_color=self.color,
            on_click=lambda e: self.on_click(e)
        )

        return ic

    @abstractmethod
    def on_click(self, e):
        ...


class TableActionBtnDone(SimpleIconButton):
    def __init__(self, page: Page, icon: str, ap_id, aval_id, table, diseabled_=False, color: str = colors.PRIMARY):
        super().__init__(page, icon, [None], color=colors.GREY if diseabled_ else color)
        self.ap_id = ap_id
        self.aval_id = aval_id
        self.table = table
        self.diseabled_ = diseabled_
        self.get.disabled = self.diseabled_

    def on_click(self, e: ControlEvent):
        ad = AlertDialog(
            title=Text(value='Confirmação', font_family='nunito'),
            content=Text(value='Deseja marcar a consulta como realizada?', font_family='nunito'),
            actions=[
                TextButton(text='Sim', on_click=lambda e: _yes()),
                TextButton(text='Cancelar', on_click=lambda e: _no()),
            ],
            actions_alignment=MainAxisAlignment.END
        )

        self.page.open(ad)

        def _yes():
            Appointment(self.page).update_appointment(self.ap_id, 'concluído')
            DocAvailability(self.page).update_availability(aval_id=self.aval_id, new_value=True)
            notify(self.page, 'Consultada marcada como realizada', icons.DONE_ROUNDED)
            self.page.close(ad)
            self.table.populate_table()
            self.page.update()

        def _no():
            self.page.close(ad)


class TableActionBtnCancel(SimpleIconButton):
    def __init__(self, page: Page, icon: str, ap_id, aval_id, table, diseabled_=False, color: str = colors.PRIMARY):
        super().__init__(page, icon, [None], color=colors.GREY if diseabled_ else color)
        self.ap_id = ap_id
        self.aval_id = aval_id
        self.table = table
        self.diseabled_ = diseabled_
        self.get.disabled = self.diseabled_

    def on_click(self, e: ControlEvent):
        ad = AlertDialog(
            title=Text(value='Confirmação', font_family='nunito'),
            content=Text(value='Deseja CANCELAR a consulta?', font_family='nunito'),
            actions=[
                TextButton(text='Sim', on_click=lambda e: _yes()),
                TextButton(text='Não', on_click=lambda e: _no()),
            ],
            actions_alignment=MainAxisAlignment.END
        )

        self.page.open(ad)

        def _yes():
            Appointment(self.page).update_appointment(self.ap_id, 'cancelado')
            DocAvailability(self.page).update_availability(aval_id=self.aval_id, new_value=True)
            notify(self.page, 'A consulta foi cancelada', icons.CANCEL_ROUNDED)
            self.page.close(ad)
            self.table.populate_table()
            self.page.update()

        def _no():
            self.page.close(ad)
