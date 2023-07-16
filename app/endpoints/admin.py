import typing

from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from common.base_endpoints import JwtEndpoint
from common.exceptions import AuthException, SessionExpireException

from .. import models
from ..extensions import jwt


class LoginEndpoint(JwtEndpoint):
    JWT_KEY = "admin_token"
    jwt = jwt

    async def post(self, req: Request) -> JSONResponse:
        data = await req.json()
        user = await models.AdminUser.get(username=data["username"])
        if user.password != data["password"]:
            raise AuthException("Wrong username or password")

        self.jwt_data = {"user_id": user.id}
        return JSONResponse({"name": user.username, "avatar": ""})


class AuthRequireEndpoint(JwtEndpoint):
    JWT_KEY = LoginEndpoint.JWT_KEY
    jwt = jwt
    user: models.AdminUser

    async def on_request(self, req: Request):
        await super().on_request(req)
        if not self.jwt_data:
            raise SessionExpireException("Login required")

        self.user = await models.AdminUser.get(id=self.jwt_data["user_id"])
        assert self.user


class UserEndpoint(AuthRequireEndpoint):
    async def get(self, req: Request) -> JSONResponse:
        user_id = req.query_params.get("id")
        user = await models.AdminUser.get(id=user_id)
        return JSONResponse(user.to_dict())


class SingleChoiceEndpoint(AuthRequireEndpoint):
    async def get_all(
        self, status: int, page: int, size: int
    ) -> typing.List[models.SingleChoice]:
        return (
            await models.SingleChoice.filter(status=status)
            .all()
            .offset((page - 1) * size)
            .limit(size)
            .only("id", "question", "level_id", "category_id")
        )

    async def get_detail(self, pk: int) -> models.SingleChoice:
        return await models.SingleChoice.filter(id=pk).first()

    async def get(self, req: Request) -> JSONResponse:
        pk = int(req.query_params.get("id", 0))
        page = int(req.query_params.get("page", 1))
        size = int(req.query_params.get("size", 10))
        status = int(req.query_params.get("status", 1))
        if pk:
            sc = await self.get_detail(pk)
            return JSONResponse(sc.to_dict())

        scs = await self.get_all(status, page, size)
        return JSONResponse([sc.to_dict() for sc in scs])

    async def post(self, req: Request) -> JSONResponse:
        data = await req.json()
        sc = await models.SingleChoice.create(
            question=data["question"],
            choice_a=data["choice_a"],
            choice_b=data["choice_b"],
            choice_c=data["choice_c"],
            choice_d=data["choice_d"],
            choice_right=data["choice_right"],
            desc=data["desc"],
            level_id=data["level_id"],
            category_id=data["category_id"],
            status=data["status"],
        )
        return JSONResponse(sc.to_dict())

    async def put(self, req: Request):
        data = await req.json()
        sc_id = data.pop("id")
        sc = await models.SingleChoice.get(id=sc_id)
        for k, v in data.items():
            setattr(sc, k, v)
        await sc.save()
        return JSONResponse(sc.to_dict())

    async def delete(self, req: Request):
        data = await req.json()
        await models.SingleChoice.filter(id=data["id"]).update(status=0)
        return JSONResponse({"status": "success"})


class LevelEndpoint(AuthRequireEndpoint):
    async def get(self, req: Request) -> JSONResponse:
        levels = await models.Level.all()
        return JSONResponse([l.to_dict() for l in levels])

    async def post(self, req: Request):
        data = await req.json()
        level = await models.Level.create(name=data["name"])
        return JSONResponse(level.to_dict())

    async def put(self, req: Request) -> JSONResponse:
        data = await req.json()
        level = await models.Level.get(id=data["id"])
        level.name = data["name"]
        await level.save()
        return JSONResponse(level.to_dict())

    async def delete(self, req: Request) -> JSONResponse:
        data = await req.json()
        await models.Level.filter(id=data["id"]).delete()
        return JSONResponse({})


class CategoryEndpoint(AuthRequireEndpoint):
    async def get(self, req: Request) -> JSONResponse:
        cs = await models.Category.all()
        return JSONResponse([c.to_dict() for c in cs])

    async def post(self, req: Request):
        data = await req.json()
        c = await models.Category.create(name=data["name"])
        return JSONResponse(c.to_dict())

    async def put(self, req: Request) -> JSONResponse:
        data = await req.json()
        c = await models.Category.get(id=data["id"])
        c.name = data["name"]
        await c.save()
        return JSONResponse(c.to_dict())

    async def delete(self, req: Request) -> JSONResponse:
        data = await req.json()
        await models.Category.filter(id=data["id"]).delete()
        return JSONResponse({})
