def validate_cpf(cpf: str) -> bool:
    if len(cpf) != 11:
        return False

    # Remove comment in production
    # if cpf == cpf[0] * len(cpf):
    #     return False

    def calcular_digito(cpf, peso):
        soma = sum(int(digito) * peso for digito, peso in zip(cpf, range(peso, 1, -1)))
        resto = soma % 11
        return '0' if resto < 2 else str(11 - resto)

    digito1 = calcular_digito(cpf[:9], 10)
    digito2 = calcular_digito(cpf[:9] + digito1, 11)

    return cpf[-2:] == digito1 + digito2


def check_empty_fileds(controls: list):
    is_valid = True

    for c in controls[0:len(controls)-1:]:
        if c.value == '' or c.value is None or c.value == 'Data nasc.':
            is_valid = False

    for c in controls[-1][2::]:
        if c.value == '' or c.value is None:
            is_valid = False

    return is_valid
