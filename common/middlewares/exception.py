from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
from starlette.types import Receive, Scope, Send

from .. import exceptions
from .base import BaseMiddleware


class ExceptionMiddleware(BaseMiddleware):
    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        try:
            await self.app(scope, receive, send)
        except Exception as exc:
            if scope["type"] == "http":
                await self.handle(exc)(scope, receive, send)
            else:
                pass  # todo: log
            raise exc from None

    def handle(self, exc: Exception) -> JSONResponse:
        code = 500
        msg = "SERVER ERROR"
        status = "error"
        if self.debug:
            msg = str(exc)

        if isinstance(exc, HTTPException):
            code = exc.status_code
            msg = exc.detail
        elif isinstance(exc, exceptions.AuthException):
            code = exc.HTTP_STATUS_CODE
            msg = str(exc)
        else:
            pass  # todo:

        return JSONResponse(
            {"data": {}, "msg": msg, "status": status}, status_code=code
        )
