import os
import uuid
import jwt
import datetime


def generar_uuid():
    # Genera un UUID basado en el tiempo
    return str(uuid.uuid4())

def generar_jwt(idUsuario: int, minutosDuracion: int):
    secret_key = os.getenv("SECRET_KEY","VAMOS_CHILENOS")  # LEE LA CLAVE DESDE EL .env

    if not secret_key:
        raise ValueError("SECRET_KEY no está definida en las variables de entorno")

    # Crea un token JWT con una fecha de expiración
    payload = {
        'usuario_id': idUsuario,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=minutosDuracion)
    }

    # Genera el token JWT
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token
