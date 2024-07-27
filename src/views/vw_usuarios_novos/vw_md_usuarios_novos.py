# -*- coding: utf-8 -*-
import datetime
from flet import *
from abc import ABC, abstractmethod
from src.models.md_users import Employee, Doctor, Patient
from src.controls.gui_utils import notify
from src.controls.ctrl_externals import find_cep
from src.models.md_doctor_availability import DocAvailability
from src.controls.ctrl_novos_usuarios import check_empty_fileds
from src.models.md_credentials import Credentials

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
            dd.options.append(
                dropdown.Option(op)
            )

        return dd


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


class SearchCepButton(SimpleIconButton):
    def __init__(self, page: Page, icon: str, controls: list, color: str = colors.PRIMARY):
        super().__init__(page, icon, controls, color)
        self.get.style = ButtonStyle(
            overlay_color='transparent'
        )

        self.txt_cep = controls[0]
        self.txt_street = controls[1]
        self.txt_number = controls[2]
        self.txt_neighborhood = controls[3]
        self.txt_city = controls[4]
        self.txt_country = controls[5]
        self.txt_state = controls[6]

    def on_click(self, e):
        if len(self.txt_cep.get.value) != 8:
            return

        data = find_cep(self.txt_cep.get.value)

        self.txt_street.get.value = data[0]
        self.txt_neighborhood.get.value = data[1]
        self.txt_city.get.value = data[2]
        self.txt_state.get.value = data[3]
        self.txt_country.get.value = data[4]
        self.page.update()


class DoctorAvalTable:
    def __init__(self, page: Page, controls: list):
        self.page = page
        self.controls = controls
        self._add_button = IconButton(icon=icons.ADD_ROUNDED, icon_color=colors.YELLOW,
                                      on_click=lambda e: self.add_new_aval(e))

        self.date_input = Container(
            content=Text('data', text_align=TextAlign.CENTER),
            border=border.all(1, BORDER_COLORS),
            border_radius=BORDER_RADIUS,
            padding=padding.only(top=5, bottom=5, right=20, left=20),
            width=125,
            on_click=lambda e: self.page.open(self.date_picker),
        )

        self.time_input = Container(
            content=Text('hora', text_align=TextAlign.CENTER),
            border=border.all(1, BORDER_COLORS),
            border_radius=BORDER_RADIUS,
            padding=padding.only(top=5, bottom=5, right=20, left=20),
            width=125,
            on_click=lambda e: self.page.open(self.time_picker)
        )

        self.date_picker = DatePicker(
            date_picker_entry_mode=DatePickerEntryMode.CALENDAR_ONLY,
            cancel_text='Cancelar',
            help_text='Escolha a data',
            on_change=lambda e: self._fill_date_from_picker(e)
        )

        self.time_picker = TimePicker(
            time_picker_entry_mode=TimePickerEntryMode.DIAL_ONLY,
            help_text='Escolha a hora',
            cancel_text='Cancelar',
            on_change=lambda e: self._fill_time_from_picker(e)
        )

        self.get, self.get_container = self._get()

    def populate_table(self):
        self.get.rows.clear()
        id_ = self.controls[0].get.value

        doctor_avals = DocAvailability(self.page).read_availability(columns="aval_date, aval_hour, is_available, "
                                                                            "aval_id",
                                                                    condition=f"doctor_id = {id_} AND is_enabled = {True}")

        if doctor_avals is None or len(doctor_avals) < 1:
            return

        for aval in doctor_avals:
            self.add_new_aval_line(*aval)

    def _get(self) -> tuple[DataTable, Container]:
        dt = DataTable(
            data_row_min_height=24,
            horizontal_lines=BorderSide(width=.5, color=colors.PRIMARY),
            columns=[
                DataColumn(label=Row([Icon(name=icons.CALENDAR_TODAY), Text(value='Data', font_family='nunito')]),
                           tooltip='Dia da disponibilidade médica'),
                DataColumn(
                    label=Row([Icon(name=icons.ACCESS_TIME_ROUNDED), Text(value='Hora', font_family='nunito')]),
                    tooltip='Hora da disponibilidade médica'),

                DataColumn(
                    label=Row([Icon(name=icons.EVENT_AVAILABLE), Text(value='Status',
                                                                      font_family='nunito')]),
                    tooltip='Status da disponibilidade'),

                DataColumn(label=Text(''))

            ]
        )

        dt_container = Container(
            padding=padding.only(top=20),
            content=Column(
                spacing=20,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Container(
                        content=Row([self.date_input, self.time_input, self._add_button],
                                    alignment=MainAxisAlignment.CENTER),
                        border=border.only(bottom=BorderSide(2, BORDER_COLORS)),
                        padding=padding.only(top=5, bottom=5, right=10, left=10),
                        width=400,
                    ),
                    Row([Column(controls=[dt], height=250, scroll=ScrollMode.AUTO)],
                        alignment=MainAxisAlignment.CENTER),
                ]
            )
        )

        return dt, dt_container

    def _fill_time_from_picker(self, e: ControlEvent):
        time = datetime.datetime.strptime(e.data, '%H:%M').time()
        self.time_input.content.value = time.strftime('%H:%M')
        self.page.update()

    def _fill_date_from_picker(self, e: ControlEvent):
        date = datetime.datetime.strptime(e.data[:10:], '%Y-%m-%d').date()
        self.date_input.content.value = date.strftime('%d/%m/%Y')
        self.page.update()

    def add_new_aval(self, e: ControlEvent):
        val_date = self.date_input.content.value
        val_time = self.time_input.content.value

        if val_date == 'data' or val_time == 'hora':
            return

        DocAvailability(self.page, doctor_id=self.controls[0].get.value, aval_date=val_date,
                        aval_hour=val_time).create_availability()

        self.date_input.content.value = 'data'
        self.time_input.content.value = 'hora'

        self.populate_table()
        self.page.update()

    def add_new_aval_line(self, date: datetime.date, time: datetime.time, aval: bool, aval_id: int,
                          normal: bool = True):
        if normal:
            formated_date = date.strftime(format='%d/%m/%Y')
            formated_time = time.strftime(format='%H:%M')
            formated_aval = 'disponível' if aval else 'reservado'

            def remove_aval(e: ControlEvent):
                DocAvailability(self.page).delete_availability(aval_id)
                self.populate_table()
                self.page.update()

            self.get.rows.append(
                DataRow(cells=[
                    DataCell(
                        content=Text(value=formated_date, font_family='nunito')
                    ),

                    DataCell(
                        content=Text(value=formated_time, font_family='nunito')
                    ),

                    DataCell(
                        content=Text(value=formated_aval, font_family='nunito',
                                     color=colors.GREEN if aval else colors.RED)
                    ),

                    DataCell(
                        content=IconButton(
                            icon=icons.DELETE_FOREVER_ROUNDED, scale=.8, on_click=lambda e: remove_aval(e),
                            icon_color=colors.GREY_400 if aval else colors.GREY_700, disabled=not aval
                        )
                    )

                ])
            )
            return

        self.get.rows.append(
            DataRow(
                ...
            )
        )


class SimpleTextButton:
    def __init__(self, page: Page, text: str, controls: list, width: int = 200, main_btn: bool = False):
        self.page = page

        self.controls = controls
        self.text = text
        self.width = width
        self.main_btn = main_btn

        self.get = self._get()

    def _get(self):
        if self.main_btn:
            tb = TextButton(
                content=Text(value=self.text, color=colors.ON_PRIMARY,
                             font_family='nunito2'),
                width=self.width,
                style=ButtonStyle(
                    bgcolor=colors.PRIMARY,
                ), on_click=lambda e: self._on_click(e)
            )
            return tb

        tb = OutlinedButton(
            content=Text(value=self.text, color=colors.PRIMARY, font_family='nunito2'),
            width=self.width, on_click=lambda e: self._on_click(e)
        )

        return tb

    def _on_create_user(self):
        if not check_empty_fileds(self.controls):
            notify(self.page, message='Todos os campos são obrigatório. Preencha-os\n\nDica: Preencha os campos que não'
                                      ' devem conter informações com um traço (-)', icon=icons.ERROR_ROUNDED)
            return

        user_type = self.controls[0].value
        fullname = self.controls[1].value
        cpf = self.controls[2].value
        gender = self.controls[3].value if self.controls[3].value != '-' else None
        telephone_1 = self.controls[4].value
        telephone_2 = self.controls[5].value if self.controls[5].value != '-' else None
        email = self.controls[6].value
        birthdate = self.controls[7].value
        cep = self.controls[8].value
        street = self.controls[9].value
        number = self.controls[10].value
        neighborhood = self.controls[11].value
        city = self.controls[12].value
        country = self.controls[13].value
        state = self.controls[14].value
        complement = self.controls[15].value if self.controls[15].value != '-' else None
        comments = self.controls[16].value if self.controls[16].value != '-' else None
        created_by = self.controls[17].value
        login = self.controls[18].value
        password = self.controls[19].value
        confirm_password = self.controls[20].value

        if Credentials(self.page).do_already_exists(login=login):
            notify(self.page, message='A identificação informada já existe. Escolha outra', icon=icons.ERROR_ROUNDED)
            return

        data = [
            cpf,
            fullname,
            birthdate,
            telephone_1,
            email,
            cep,
            street,
            number,
            neighborhood,
            city,
            state,
            country,
            user_type,
            gender,
            telephone_2,
            complement,
            comments,
            created_by,
            login,
            password,
            confirm_password
        ]

        match self.controls[0].value:
            case 'funcionário':
                role = self.controls[21][2].value
                Employee(self.page, *data[0:17:], role=role, password=password, login=login).create_employee()
            case 'médico':
                crm = self.controls[21][2].value
                price = self.controls[21][3].value
                specialty = self.controls[21][4].value
                Doctor(self.page, *data[0:17:], crm=crm, specialty=specialty, price=price, password=password, login=login).create_doctor()
            case 'paciente':
                insurance = self.controls[21][2].value
                Patient(self.page, *data[0:17:], insurance=insurance, password=password, login=login).create_patient()

    def _on_click(self, e: ControlEvent):
        if self.main_btn:
            self._on_create_user()
            return

        self.controls[3].value = None

        login = self.controls[0].get
        password = self.controls[1].get
        confirm_password = self.controls[2].get

        if not login.value != '':
            notify(page=self.page, message='Preencha o campo de identificação.\nEle pode ser um nome de usuário ou um e-mail.'
                                           ' Cosulte seu gerente antes de escolher', icon=icons.ERROR_ROUNDED)
            return

        if not password.value != '':
            notify(page=self.page,
                   message='Preencha os campos de senha', icon=icons.ERROR_ROUNDED)
            return

        if password.value != confirm_password.value:
            notify(page=self.page,
                   message='As senhas não coincidem', icon=icons.ERROR_ROUNDED)
            return

        self.controls[3].value = True

