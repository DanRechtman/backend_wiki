from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from data.testing import dataTest

router = APIRouter(
    prefix=""
)
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def read_root(request:Request):
    data=dataTest()
    data.insertData(request.client.host)


    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )