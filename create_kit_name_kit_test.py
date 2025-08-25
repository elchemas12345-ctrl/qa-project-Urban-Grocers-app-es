# tests/create_kit_name_kit_test.py

import pytest
import data
from sender_stand_request import get_new_user_token, post_new_client_kit


def get_kit_body(name):
    """Devuelve el cuerpo del kit con el name indicado."""
    return {"name": name}


def positive_assert(kit_body):
    """Valida casos en los que se espera 201 y coincidencia de name."""
    token = get_new_user_token()
    response = post_new_client_kit(kit_body, token)

    assert response.status_code == 201, f"Se esperaba 201, se obtuvo {response.status_code}"
    response_json = response.json()
    assert response_json["name"] == kit_body["name"], \
        f"El campo name no coincide. Enviado: {kit_body['name']}, Recibido: {response_json.get('name')}"


def negative_assert_code_400(kit_body):
    """Valida casos en los que se espera error 400."""
    token = get_new_user_token()
    response = post_new_client_kit(kit_body, token)
    assert response.status_code == 400, f"Se esperaba 400, se obtuvo {response.status_code}"


# ========== PRUEBAS ==========

# 1. Nombre con 1 carácter
def test_create_kit_1_char():
    positive_assert(get_kit_body("a"))


# 2. Nombre con 511 caracteres
def test_create_kit_511_chars():
    positive_assert(get_kit_body(data.name_511))


# 3. Nombre vacío (0 caracteres)
def test_create_kit_empty_name():
    negative_assert_code_400(get_kit_body(""))


# 4. Nombre con 512 caracteres
def test_create_kit_512_chars():
    negative_assert_code_400(get_kit_body(data.name_512))


# 5. Caracteres especiales permitidos
def test_create_kit_special_chars():
    positive_assert(get_kit_body("№%@,"))


# 6. Nombre con espacios
def test_create_kit_spaces():
    positive_assert(get_kit_body(" A Aaa "))


# 7. Nombre con números
def test_create_kit_numbers():
    positive_assert(get_kit_body("123"))


# 8. Parámetro "name" no se pasa
def test_create_kit_no_name_param():
    negative_assert_code_400({})  # cuerpo vacío


# 9. Tipo de parámetro diferente (número en vez de string)
def test_create_kit_name_as_number():
    negative_assert_code_400(get_kit_body(123))
