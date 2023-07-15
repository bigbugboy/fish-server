import typing

from starlette.types import ASGIApp

from common.middlewares.exception import ExceptionMiddleware

MIDDLEWARES: typing.List[typing.Type[ASGIApp]] = [
    ExceptionMiddleware,
]
