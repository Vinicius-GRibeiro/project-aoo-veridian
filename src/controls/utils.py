# -*- coding: utf-8 -*-
def convert_money_from_db_to_float_money(value: str) -> float:
    stringed_float = value.removeprefix('R$ ').replace('.', '').replace(',', '.')
    return float(stringed_float)
