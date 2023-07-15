from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.models import SingleChoice


class Hello(HTTPEndpoint):
    async def get(self, _):
        return Response("hello")


class SingleChoiceEndpoint(HTTPEndpoint):
    async def get(self, req: Request):
        qid = req.query_params.get("qid")
        scs = await SingleChoice.all()
        return JSONResponse([sc.to_dict() for sc in scs])

    async def post(self, req: Request):
        data = await req.json()
        sc = await SingleChoice.create(**data)
        return JSONResponse(sc.to_dict())
