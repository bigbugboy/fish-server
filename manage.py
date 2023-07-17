import asyncio
import click
from contextlib import contextmanager

from IPython import embed
from tortoise.contrib.starlette import register_tortoise
from uvicorn import run as _run

import settings
from app.app import App
from app.middlewares import MIDDLEWARES
from app.routes import ROUTES


loop = asyncio.get_event_loop()
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


@contextmanager
def app_life():
    loop.run_until_complete(app.startup())
    yield
    loop.run_until_complete(app.shutdown())


@click.group()
def main():
    pass


@main.command()
def shell():
    ctx = {"app": app}
    with app_life():
        # 参数using的作用，可以在shell中直接使用await
        embed(user_ns=ctx, using=lambda c: loop.run_until_complete(c), colors="neutral")


@main.command()
@click.option('--host', default='127.0.0.1')
@click.option('--port', default=8000)
def run(host, port):
    _run(app, host=host, port=port)


# 两种方式启动项目
if __name__ == '__main__':
    # 使用 python manage.py run
    main()
else:
    # 使用 uvicorn manage:app
    pass
