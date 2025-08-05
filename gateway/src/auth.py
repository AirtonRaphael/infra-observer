import jwt
from jwt.exceptions import ExpiredSignatureError, PyJWTError

with open("public.pem", "rb") as f:
    PUBLIC_KEY = f.read()


def validate_jwt(encoded_jwt: str | None):
    try:
        payload = jwt.decode(encoded_jwt, PUBLIC_KEY, algorithms=['RS256'])
        return payload
    except ExpiredSignatureError:
        return
    except PyJWTError:
        return
