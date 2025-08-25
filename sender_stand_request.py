# sender_stand_request.py

import uuid
import requests
import configuration as config
import data

def _url(path: str) -> str:
    # Maneja bien las barras por si la base trae / al final
    return f"{config.URL_SERVICE.rstrip('/')}{path}"

def post_new_user(user_body: dict) -> requests.Response:
    return requests.post(_url(config.CREATE_USER_PATH),
                         json=user_body,
                         headers=config.HEADERS)

def post_new_client_kit(kit_body: dict, auth_token: str) -> requests.Response:
    headers = dict(config.HEADERS)
    # IMPORTANTE: Authorization sin errores de escritura
    headers["Authorization"] = auth_token  # Si tu API requiere "Bearer <token>", cámbialo aquí.
    return requests.post(_url(config.CREATE_KIT_PATH),
                         json=kit_body,
                         headers=headers)

def get_new_user_token() -> str:
    """Crea un usuario y devuelve su authToken."""
    body = data.create_user_body.copy()
    # Evitar colisiones si el backend valida unicidad (teléfono, etc.)
    body["phone"] = "+52" + f"{uuid.uuid4().int % 10**10:010d}"
    resp = post_new_user(body)
    resp.raise_for_status()
    # La clave comúnmente usada en este proyecto es 'authToken'
    token = resp.json().get("authToken")
    if not token:
        raise RuntimeError(f"No se recibió authToken. Respuesta: {resp.status_code} {resp.text}")
    return token
