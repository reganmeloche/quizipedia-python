from six.moves.urllib.request import urlopen
from functools import wraps
from flask import Flask, request, jsonify, _request_ctx_stack
import json
import jwt

from .helpers.exceptions import AuthError

class AuthLib():
    def __init__(self, auth_options):
        self.__auth_options = auth_options
    
    def generate_token(self):
        encoded_jwt = jwt.encode(
            {"username": self.__auth_options.api_user}, 
            self.__auth_options.jwt_secret, 
            algorithm="HS256"
        )
        return encoded_jwt

    def requires_auth(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            encoded_jwt = get_token_auth_header()
            try:
                payload = jwt.decode(encoded_jwt, self.__auth_options.jwt_secret, algorithms=["HS256"])
                # _request_ctx_stack.top.current_user = payload ## For adding to req - not needed now
                assert payload['username'] == self.__auth_options.api_user
                return f(*args, **kwargs)
            except Exception:
                raise AuthError({
                    "code": "invalid_header",
                    "description": "Unable to parse authentication token."
                }, 401)
            
        return decorated


### HELPERS ###

def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({
            "code": "authorization_header_missing",
            "description": "Authorization header is expected"
        }, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({
            "code": "invalid_header",
            "description": "Authorization header must start with Bearer"
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            "code": "invalid_header",
            "description": "Token not found"
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            "code": "invalid_header",
            "description": "Authorization header must be Bearer token"
        }, 401)

    token = parts[1]
    return token
