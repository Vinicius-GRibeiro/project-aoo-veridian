# -*- coding: utf-8 -*-
from flet import *
from src.models.md_users import User, Doctor
from abc import ABC, abstractmethod
from src.models.md_doctor_availability import DocAvailability
import datetime

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


class PatientsTable:
    def __init__(self, page: Page):
        self.page = page
        self.selected_row = None
        self.get = self._get()
        self.populate_table(conditions="user_type = 'paciente'")

    def populate_table(self, conditions=None):
        if conditions is not None and conditions != '':
            users = User().read_user(columns="user_id, cpf, fullname", order_by='fullname',
                                     condition=conditions)
        else:
            users = User().read_user(columns="user_id, cpf, fullname", order_by='fullname')

        self.get.rows.clear()

        if users is None or len(users) < 1:
            return

        for user in users:
            self.add_new_user_line(*user)

    def _get(self) -> DataTable:
        dt = DataTable(
            column_spacing=15,
            width=400,
            horizontal_lines=BorderSide(width=.5, color=colors.PRIMARY),
            columns=[
                DataColumn(label=Row([Icon(name=icons.GRID_3X3_ROUNDED), Text(value='ID', font_family='nunito')]),
                           tooltip='Identificação única do usuário no sistema'),

                DataColumn(
                    label=Row([Icon(name=icons.FEATURED_PLAY_LIST_ROUNDED), Text(value='CPF', font_family='nunito')])),

                DataColumn(label=Row([Icon(name=icons.PERSON_ROUNDED), Text(value='Nome', font_family='nunito')])),
            ]
        )
        return dt

    def add_new_user_line(self, user_id: str, cpf: str, nome: str):
        self.get.rows.append(
            DataRow(cells=[
                DataCell(
                    content=Text(value=user_id, font_family='nunito')
                ),

                DataCell(
                    content=Text(value=cpf, font_family='nunito')
                ),

                DataCell(
                    content=Text(value=nome, font_family='nunito')
                ),
            ], on_select_changed=lambda e: self.__on_how_selected(e, user_id)
            )
        )

    def __on_how_selected(self, e: ControlEvent, patient_id):
        for row in self.get.rows:
            if row.selected:
                if row.cells[0].content.value != patient_id:
                    row.selected = False

        if e.control.selected:
            e.control.selected = False
            self.selected_row = None
        else:
            e.control.selected = True
            self.selected_row = patient_id

        self.page.update()


class DoctorAvalTable:
    def __init__(self, page: Page):
        self.page = page
        self.selected_row = None
        self.get = self._get()

    def populate_table_(self, doctor_id: int):

        avals = DocAvailability(self.page).read_availability(columns='aval_id, aval_date, aval_hour',
                                                             condition=f"doctor_id = {doctor_id}"
                                                                       f" AND is_available = {True}"
                                                                       f" AND is_enabled = {True}")

        if avals is None or len(avals) < 1:
            return

        self.get.rows.clear()

        for aval in avals:
            self.add_new_aval_line(*aval)

    def _get(self) -> DataTable:
        dt = DataTable(
            data_row_min_height=24,
            horizontal_lines=BorderSide(width=.5, color=colors.PRIMARY),
            columns=[
                DataColumn(label=Row([Icon(name=icons.GRID_3X3_ROUNDED), Text(value='ID', font_family='nunito')])),

                DataColumn(label=Row([Icon(name=icons.CALENDAR_TODAY), Text(value='Data', font_family='nunito')])),

                DataColumn(label=Row([Icon(name=icons.ACCESS_TIME_ROUNDED), Text(value='Hora', font_family='nunito')])),

            ]
        )

        return dt

    def add_new_aval_line(self, aval_id, date: datetime.date, time: datetime.time):
        formated_date = date.strftime(format='%d/%m/%Y')
        formated_time = time.strftime(format='%H:%M')

        self.get.rows.append(
            DataRow(cells=[
                DataCell(
                    content=Text(value=aval_id, font_family='nunito')
                ),

                DataCell(
                    content=Text(value=formated_date, font_family='nunito')
                ),

                DataCell(
                    content=Text(value=formated_time, font_family='nunito')
                ),
            ], on_select_changed=lambda e: self._on_row_change(e, aval_id))
        )
        return

    def _on_row_change(self, e: ControlEvent, doc_aval_id):
        for row in self.get.rows:
            if row.selected:
                if row.cells[0].content.value != doc_aval_id:
                    row.selected = False

        if e.control.selected:
            e.control.selected = False
            self.selected_row = None
        else:
            e.control.selected = True
            self.selected_row = doc_aval_id

        self.page.update()


class DoctorsTable:
    def __init__(self, page: Page, aval_table: DoctorAvalTable):
        self.page = page
        self.selected_row = None
        self.aval_table = aval_table
        self.get = self._get()

        self.populate_table(conditions="user_type = 'médico'")

    def populate_table(self, conditions=None, reverse: bool = False):
        if not reverse:
            if conditions is not None and conditions != '':
                docs_id_and_name = User().read_user(columns="user_id, fullname", order_by='fullname',
                                                    condition=conditions)
            else:
                docs_id_and_name = User().read_user(columns="user_id, fullname", order_by='fullname')

            if docs_id_and_name is None:
                return

            self.get.rows.clear()

            for doc in docs_id_and_name:
                specialty = Doctor(self.page).read_doctor(columns='specialty', user_id=doc[0])[0][0]
                self.add_new_user_line(doc[0], doc[1], specialty)

            return

        docs_id_and_specialty = Doctor(self.page).read_doctor(columns='user_id, specialty', condition=conditions)
        if len(docs_id_and_specialty) <= 0:
            return

        self.get.rows.clear()

        for doc in docs_id_and_specialty:
            name = User(self.page).read_user(columns='fullname', user_id=doc[0])[0][0]
            self.add_new_user_line(doc[0], name, doc[1])

    def _get(self) -> DataTable:
        dt = DataTable(
            column_spacing=15,
            width=400,
            horizontal_lines=BorderSide(width=.5, color=colors.PRIMARY),
            columns=[
                DataColumn(label=Row([Icon(name=icons.GRID_3X3_ROUNDED), Text(value='ID', font_family='nunito')]),
                           tooltip='Identificação única do usuário no sistema'),

                DataColumn(
                    label=Row([Icon(name=icons.FEATURED_PLAY_LIST_ROUNDED),
                               Text(value='Especialidade', font_family='nunito')])),

                DataColumn(label=Row([Icon(name=icons.PERSON_ROUNDED), Text(value='Médico', font_family='nunito')])),
            ],
        )
        return dt

    def add_new_user_line(self, user_id: str, name: str, specialty: str):
        self.get.rows.append(
            DataRow(cells=[
                DataCell(
                    content=Text(value=user_id, font_family='nunito')
                ),

                DataCell(
                    content=Text(value=specialty, font_family='nunito')
                ),

                DataCell(
                    content=Text(value=name, font_family='nunito')
                ),
            ], on_select_changed=lambda e: self.__on_row_selected(e, user_id)
            )
        )

    def __on_row_selected(self, e: ControlEvent, doc_id):
        for row in self.get.rows:
            if row.selected:
                if row.cells[0].content.value != doc_id:
                    row.selected = False
                    self.aval_table.get.rows.clear()

        if e.control.selected:
            e.control.selected = False
            self.selected_row = None
        else:
            e.control.selected = True
            self.selected_row = doc_id

        if e.control.selected:
            self.aval_table.populate_table_(doctor_id=doc_id)
        else:
            self.aval_table.get.rows.clear()

        self.page.update()


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


class SearchButton(SimpleIconButton):
    def __init__(self, page: Page, icon: str, controls: list, color: str = colors.PRIMARY):
        super().__init__(page, icon, controls, color)
        self.table: PatientsTable = controls[0]
        self.name: Txt = controls[1]
        self.cpf: Txt = controls[2]

    def on_click(self, e: ControlEvent):
        name, cpf = self.name.get.value, self.cpf.get.value
        condition = ''

        queries = [
            f" cpf = '{cpf}'" if cpf != '' else '',
            f" fullname ILIKE '%{name}%'" if name != '' else '',
            f" user_type = 'paciente'"
        ]

        for query in queries:
            condition += f" AND {query}" if (len(condition) > 0 and query != '') else query if query != '' else ''

        self.table.populate_table(conditions=condition)
        self.page.update()


class RefreshButton(SimpleIconButton):
    def __init__(self, page: Page, icon: str, controls: list, user_type: str, color: str = colors.PRIMARY):
        super().__init__(page, icon, controls, color)

        self.type = user_type

        if self.type == 'paciente':
            self.table = controls[0]
            self.name: Txt = controls[1]
            self.cpf: Txt = controls[2]
        elif self.type == 'médico':
            self.doctors_table: DoctorsTable = controls[0]

    def on_click(self, e: ControlEvent):
        if self.type == 'paciente':
            self.table.populate_table(conditions="user_type = 'paciente'")
            self.name.get.value = ''
            self.cpf.get.value = ''
            self.page.update()
        elif self.type == 'médico':
            self.doctors_table.populate_table(conditions="user_type = 'médico'")
            self.page.update()
