# -*- coding: utf-8 -*-
import datetime
from flet import *
from abc import ABC, abstractmethod
from src.controls.gui_utils import notify, modal
from src.controls.ctrl_usuarios import validate_user_fields
from src.models.md_doctor_availability import DocAvailability
from src.models.md_users import User, Patient, Doctor, Employee

BORDER_RADIUS = 10
BORDER_COLORS = '#494D5F'


class UsersTable:
    def __init__(self, page: Page, controls: list, specific_controls: list = None):
        self.page = page
        self.controls = controls
        self.specific_controls = specific_controls
        self.get = self._get()
        self.populate_table()

    def populate_table(self, conditions=None):
        if conditions is not None and conditions != '':
            users = User().read_user(columns="user_id, cpf, fullname, user_type, user_status", order_by='fullname',
                                     condition=conditions)
        else:
            users = User().read_user(columns="user_id, cpf, fullname, user_type, user_status", order_by='fullname')

        self.get.rows.clear()

        if users is None or len(users) < 1:
            return

        for user in users:
            self.add_new_user_line(*user)

    def _get(self) -> DataTable:
        dt = DataTable(
            data_row_min_height=24,
            horizontal_lines=BorderSide(width=.5, color=colors.PRIMARY),
            columns=[
                DataColumn(label=Row([Icon(name=icons.GRID_3X3_ROUNDED), Text(value='ID', font_family='nunito')]),
                           tooltip='Identificação única do usuário no sistema'),
                DataColumn(
                    label=Row([Icon(name=icons.FEATURED_PLAY_LIST_ROUNDED), Text(value='CPF', font_family='nunito')])),
                DataColumn(label=Row([Icon(name=icons.PERSON_ROUNDED), Text(value='Nome', font_family='nunito')])),
                DataColumn(label=Row(
                    [Icon(name=icons.FORMAT_LIST_NUMBERED_ROUNDED), Text(value='Tipo', font_family='nunito')]),
                    tooltip='Indica se o usuário é funcionário, professor ou aluno'),
                DataColumn(
                    label=Row([Icon(name=icons.DO_NOT_TOUCH_ROUNDED), Text(value='Status', font_family='nunito')]),
                    tooltip='Indica se o usuário está bloqueado ou não'),
            ]
        )

        return dt

    def add_new_user_line(self, user_id: str, cpf: str, nome: str, tipo: str, condicao: bool = True):
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

                DataCell(
                    content=Text(value=tipo[0].upper(), font_family='nunito')
                ),

                DataCell(
                    content=Icon(name=icons.DONE_ROUNDED) if condicao else Icon(name=icons.BLOCK_ROUNDED)
                )
            ], on_select_changed=lambda e: self.fill_form(e, user_id))
        )

    def fill_form(self, e: ControlEvent, id_u):
        data = User().read_user(columns='cpf, user_status, fullname, birthdate, gender, email, phone_1, phone_2, '
                                        'address_zipcode, address_street, address_number, address_neighborhood, '
                                        'address_city, address_state, address_country, address_complement, comments,'
                                        'user_type, created_by', user_id=id_u)[0]
        id_ = self.controls[0]
        cpf = self.controls[1]
        status = self.controls[2]
        fullname = self.controls[3]
        birthdate = self.controls[4]
        gender = self.controls[5]
        email = self.controls[6]
        phone_1 = self.controls[7]
        phone_2 = self.controls[8]
        zip_code = self.controls[9]
        street = self.controls[10]
        number = self.controls[11]
        neighborhood = self.controls[12]
        city = self.controls[13]
        state = self.controls[14]
        country = self.controls[15]
        complement = self.controls[16]
        comments = self.controls[17]
        type_ = self.controls[18]
        created_by = self.controls[19]

        id_.get.value = id_u
        cpf.get.value = data[0]
        status.get.value = 'ATIVO' if data[1] else 'INATIVO'
        fullname.get.value = data[2]
        birthdate.get.value = data[3].strftime("%d/%m/%Y")
        gender.get.value = data[4]
        email.get.value = data[5]
        phone_1.get.value = data[6]
        phone_2.get.value = data[7]
        zip_code.get.value = data[8]
        street.get.value = data[9]
        number.get.value = data[10]
        neighborhood.get.value = data[11]
        city.get.value = data[12]
        state.get.value = data[13]
        country.get.value = data[14]
        complement.get.value = data[15]
        comments.get.value = data[16]
        type_.get.value = data[17]
        created_by.get.value = data[18]

        e.page.update()


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


class Txt:
    def __init__(self, page: Page, width: int = 330, scale: float = 1.0, read_only: bool = False, label: str = None,
                 hint: str = None):
        self.page = page
        self.hint = hint
        self.width = width
        self.scale = scale
        self.read_only = read_only
        self.label = label
        self.get = self._get()

    def _get(self) -> TextField:
        txt = TextField(
            read_only=self.read_only,
            hint_text=self.hint if self.hint is not None else None,
            label=self.label if self.label is not None else None,
            height=35,
            cursor_width=2,
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
    def __init__(self, page: Page, options: list, scale: float = 1, selected_value='todos', hint: str = None,
                 label: str = None, width: float = 200):
        self.page = page
        self.scale = scale
        self.hint = hint
        self.options = options
        self.selected_value = selected_value
        self.label = label
        self.width = width

        self.get = self._get()

    def _get(self) -> Dropdown:
        dd = Dropdown(
            value=self.selected_value,
            width=self.width,
            scale=self.scale,
            height=38,
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


class RefreshButton(SimpleIconButton):
    def __init__(self, page: Page, icon: str, controls: list, color: str = colors.PRIMARY):
        super().__init__(page, icon, controls, color)
        self.table: UsersTable = controls[0]
        self.name: Txt = controls[1]
        self.cpf: Txt = controls[2]
        self.type: Choose = controls[3]
        self.status: RadioGroup = controls[4]  # No get

    def on_click(self, e: ControlEvent):
        self.table.populate_table()
        self.name.get.value = ''
        self.cpf.get.value = ''
        self.type.get.value = 'todos'
        self.status.value = 'todos'
        self.page.update()


class SearchButton(SimpleIconButton):
    def __init__(self, page: Page, icon: str, controls: list, color: str = colors.PRIMARY):
        super().__init__(page, icon, controls, color)
        self.table: UsersTable = controls[0]
        self.name: Txt = controls[1]
        self.cpf: Txt = controls[2]
        self.type: Choose = controls[3]
        self.status: RadioGroup = controls[4]  # No get

    def on_click(self, e: ControlEvent):
        name, cpf, type, status = self.name.get.value, self.cpf.get.value, self.type.get.value, self.status.value
        condition = ''

        boolean_status = True if status == 'regulares' else False if status == 'bloqueados' else None

        queries = [
            f" cpf = '{cpf}'" if cpf != '' else '',
            f" fullname ILIKE '%{name}%'" if name != '' else '',
            f" user_type = '{type}'" if type != 'todos' else '',
            f" user_status = {boolean_status}" if boolean_status is not None else ''
        ]

        for query in queries:
            condition += f" AND {query}" if (len(condition) > 0 and query != '') else query if query != '' else ''

        self.table.populate_table(conditions=condition)
        self.page.update()


class ClearFormButton(SimpleIconButton):
    def __init__(self, page: Page, icon: str, controls: list, color: str = colors.PRIMARY):
        super().__init__(page, icon, controls, color)

        self.id_ = self.controls[0]
        self.cpf = self.controls[1]
        self.status = self.controls[2]
        self.fullname = self.controls[3]
        self.birthdate = self.controls[4]
        self.gender = self.controls[5]
        self.email = self.controls[6]
        self.phone_1 = self.controls[7]
        self.phone_2 = self.controls[8]
        self.zip_code = self.controls[9]
        self.street = self.controls[10]
        self.number = self.controls[11]
        self.neighborhood = self.controls[12]
        self.city = self.controls[13]
        self.state = self.controls[14]
        self.country = self.controls[15]
        self.complement = self.controls[16]
        self.comments = self.controls[17]
        self.type_ = self.controls[18]
        self.created_by = self.controls[19]

    def on_click(self, e):
        self.id_.get.value = ''
        self.cpf.get.value = ''
        self.status.get.value = ''
        self.fullname.get.value = ''
        self.birthdate.get.value = ''
        self.gender.get.value = '-'
        self.email.get.value = ''
        self.phone_1.get.value = ''
        self.phone_2.get.value = ''
        self.zip_code.get.value = ''
        self.street.get.value = ''
        self.number.get.value = ''
        self.neighborhood.get.value = ''
        self.city.get.value = ''
        self.state.get.value = ''
        self.country.get.value = ''
        self.complement.get.value = ''
        self.comments.get.value = ''
        self.type_.get.value = ''
        self.created_by.get.value = ''
        e.page.update()


class UpdateUserFormButton(SimpleIconButton):
    def __init__(self, page: Page, icon: str, controls: list, color: str = colors.PRIMARY):
        super().__init__(page, icon, controls, color)

        self.id_ = self.controls[0]
        self.cpf = self.controls[1]
        self.status = self.controls[2]
        self.fullname = self.controls[3]
        self.birthdate = controls[4]
        self.gender = self.controls[5]
        self.email = self.controls[6]
        self.phone_1 = self.controls[7]
        self.phone_2 = self.controls[8]
        self.zip_code = self.controls[9]
        self.street = self.controls[10]
        self.number = self.controls[11]
        self.neighborhood = self.controls[12]
        self.city = self.controls[13]
        self.state = self.controls[14]
        self.country = self.controls[15]
        self.complement = self.controls[16]
        self.comments = self.controls[17]
        self.type_ = self.controls[18]
        self.created_by = self.controls[19]

        self.pacient_insurance = self.controls[20]
        self.employee_role = self.controls[21]
        self.doctor_crm = self.controls[22]
        self.doctor_specialty = controls[23]
        self.doctor_price = controls[24]

    def on_click(self, e):
        if not validate_user_fields(self.controls[0:20:]):
            notify(self.page, 'Preencha todos os campos obrigatórios', icons.CANCEL_ROUNDED, color=colors.RED)
            return

        birth = datetime.datetime.strptime(self.birthdate.get.value, "%d/%m/%Y").date()

        User().update_user(user_id=self.id_.get.value,
                           columns=['fullname', 'cpf', 'birthdate', 'gender', 'phone_1', 'phone_2', 'email',
                                    'address_zipcode', 'address_street', 'address_number', 'address_neighborhood',
                                    'address_city', 'address_state', 'address_country', 'address_complement', 'comments'
                               , 'user_type'],
                           new_values=[self.fullname.get.value, self.cpf.get.value, birth,
                                       self.gender.get.value, self.phone_1.get.value, self.phone_2.get.value,
                                       self.email.get.value, self.zip_code.get.value, self.street.get.value,
                                       self.number.get.value, self.neighborhood.get.value, self.city.get.value,
                                       self.state.get.value, self.country.get.value, self.complement.get.value,
                                       self.comments.get.value, self.type_.get.value])

        match self.type_.get.value:
            case 'médico':
                Doctor(self.page).update_doctor(user_id=self.id_.get.value,
                                                columns=['crm', 'specialty', 'price'],
                                                new_values=[self.doctor_crm.get.value,
                                                            self.doctor_specialty.get.value,
                                                            self.doctor_price.get.value])
            case 'funcionário':
                Employee(self.page).update_employee(user_id=self.id_.get.value,
                                                    columns=['role'],
                                                    new_values=[self.employee_role.get.value])
            case 'paciente':
                Patient(self.page).update_patient(user_id=self.id_.get.value,
                                                  columns=['insurance'],
                                                  new_values=[self.pacient_insurance.get.value])

        self.id_.get.value = ''
        self.cpf.get.value = ''
        self.status.get.value = ''
        self.fullname.get.value = ''
        self.birthdate.get.value = ''
        self.gender.get.value = '-'
        self.email.get.value = ''
        self.phone_1.get.value = ''
        self.phone_2.get.value = ''
        self.zip_code.get.value = ''
        self.street.get.value = ''
        self.number.get.value = ''
        self.neighborhood.get.value = ''
        self.city.get.value = ''
        self.state.get.value = ''
        self.country.get.value = ''
        self.complement.get.value = ''
        self.comments.get.value = ''
        self.type_.get.value = ''
        self.created_by.get.value = ''
        e.page.update()

        notify(self.page, 'Dados do usuário atualizados', icons.DONE_ROUNDED, colors.GREEN)
