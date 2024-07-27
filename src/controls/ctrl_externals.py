import requests


def find_cep(cep: str):
    response = requests.get(f"https://brasilapi.com.br/api/cep/v1/{cep}")

    if response == 404:
        return

    data = response.json()
    data_values = (data['street'], data['neighborhood'], data['city'], data['state'], 'Brasil')

    return data_values
