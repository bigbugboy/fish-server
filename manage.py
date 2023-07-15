from tortoise.contrib.starlette import register_tortoise

import settings
from app.app import App
from app.middlewares import MIDDLEWARES
from app.routes import ROUTES

app = App()
app.debug = True
app.register_routes(ROUTES)
app.register_middlewares(MIDDLEWARES)

register_tortoise(
    app,
    db_url=settings.MYSQL["url"],
    modules={"models": ["app.models"]},
    generate_schemas=True,
)
