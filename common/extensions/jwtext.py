import time
import typing

import jwt
from starlette.requests import Request
from starlette.responses import Response
from starlette.websockets import WebSocket

from ..app import ExtensionMixin
from ..exceptions import SessionExpireException


class Jwt(ExtensionMixin):
    def __init__(self, secret: str, secure=False):
        self.secret = secret
        self.secure = secure

    @staticmethod
    def _get_token(req: typing.Union[Request, WebSocket], key: str) -> str:
        return req.headers.get(f"x-{key}") or req.cookies.get(key) or ""

    def _set_token(self, res: Response, key: str, token: str):
        res.headers[f"x-{key}"] = token
        res.set_cookie(
            key,
            token,
            httponly=True,
            secure=self.secure,
        )

    def get(self, req, key):
        token = self._get_token(req, key)
        if not token:
            raise SessionExpireException()

        try:
            return jwt.decode(token, self.secret, algorithms=["HS256"])
        except jwt.PyJWTError as e:
            raise SessionExpireException() from e

    def set(self, res: Response, key: str, data: typing.Dict, expire=24 * 60 * 60):
        data["exp"] = int(time.time()) + expire
        token = jwt.encode(data, self.secret)
        self._set_token(res, key, token)
