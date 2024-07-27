from flet import *


def validate_user_fields(controls: list) -> bool:
    fullname = controls[3].get.value
    birthdate = controls[4].get.value
    email = controls[6].get.value
    phone_1 = controls[7].get.value
    zip_code = controls[9].get.value
    street = controls[10].get.value
    number = controls[11].get.value
    neighborhood = controls[12].get.value
    city = controls[13].get.value
    state = controls[14].get.value
    country = controls[15].get.value

    not_null_field = [fullname, birthdate, email, phone_1, zip_code, street, state, number, neighborhood, city, country]
    not_null_validation = True

    for field in not_null_field:
        not_null_validation = False if field is None or field == '' else True

    return not_null_validation
