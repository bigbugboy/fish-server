from starlette.types import ASGIApp, Receive, Scope, Send


class BaseMiddleware:
    def __init__(self, app: ASGIApp, debug: bool = False, **_):
        self.app = app
        self.debug = debug

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        await self.app(scope, receive, send)
