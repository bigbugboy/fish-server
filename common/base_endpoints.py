import asyncio
import typing

from starlette.endpoints import HTTPEndpoint
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import Response

from . import exceptions
from .extensions.jwtext import Jwt


class BaseEndpoint(HTTPEndpoint):
    async def on_request(self, req: Request):
        pass

    async def on_response(self, res: Response):
        pass

    async def dispatch(self) -> None:
        request = Request(self.scope, receive=self.receive)
        # hook on request
        await self.on_request(request)

        # dispatch
        handler = getattr(self, request.method.lower(), self.method_not_allowed)
        is_async = asyncio.iscoroutinefunction(handler)
        if is_async:
            response = await handler(request)
        else:
            response = handler(request)

        # hook on response
        await self.on_response(response)
        await response(self.scope, self.receive, self.send)

    async def get(self, req: Request) -> Response:
        raise HTTPException(status_code=405)

    async def head(self, req: Request) -> Response:
        return await self.get(req)

    async def post(self, req: Request) -> Response:
        raise HTTPException(status_code=405)

    async def patch(self, req: Request) -> Response:
        raise HTTPException(status_code=405)

    async def put(self, req: Request) -> Response:
        raise HTTPException(status_code=405)

    async def delete(self, req: Request) -> Response:
        raise HTTPException(status_code=405)

    async def options(self, req: Request) -> Response:
        raise HTTPException(status_code=405)


class JwtEndpoint(BaseEndpoint):
    JWT_KEY = "jwt_token"
    JWT_EXPIRE = 24 * 60 * 60
    JWT_REFRESH_PERIOD = 12 * 60 * 60

    jwt_data: typing.Dict[str, typing.Any] = {}
    jwt: Jwt

    async def on_request(self, req: Request):
        await super().on_request(req)
        try:
            self.jwt_data = self.jwt.get(req, self.JWT_KEY)
        except exceptions.SessionExpireException:
            self.jwt_data = {}

    async def on_response(self, res: Response):
        await super().on_response(res)
        if self.jwt_data:
            self.jwt.set(res, self.JWT_KEY, self.jwt_data, expire=self.JWT_EXPIRE)
