import logging
import typing

from starlette.applications import Starlette
from starlette.routing import BaseRoute

from .middlewares.base import BaseMiddleware


class BaseApp(Starlette):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.started = False
        self.debug = True

    async def ready(self):
        pass

    async def startup(self):
        if not self.started:
            await self.router.startup()
            self.started = True
            self.logger.debug("Start")

    async def shutdown(self):
        if self.started:
            await self.router.shutdown()
            self.started = False
            self.logger.debug("Shutdown")

    def register_routes(self, routes: typing.List[BaseRoute]):
        self.routes.extend(routes)
        for r in routes:
            self.logger.debug(f"Add route: {r}")

    def register_extensions(self, extensions: typing.Sequence["ExtensionMixin"]):
        for ext in extensions:
            ext.init_app(self)
            self.add_event_handler("startup", ext.on_app_startup)
            self.add_event_handler("shutdown", ext.on_app_shutdown)
            self.logger.debug(f"Register extension: {ext}")
        self.add_event_handler("startup", self.ready)

    def register_middlewares(
        self, middlewares: typing.Sequence[typing.Type[typing.Any]]
    ):
        for m in middlewares:
            options: typing.Dict[str, typing.Any] = {}
            if issubclass(m, BaseMiddleware):
                options["debug"] = False
            self.add_middleware(m, **options)
            self.logger.debug(f"Register middleware {m}")


class ExtensionMixin:
    def init_app(self, app: BaseApp):
        pass

    async def on_app_startup(self):
        pass

    async def on_app_shutdown(self):
        pass
