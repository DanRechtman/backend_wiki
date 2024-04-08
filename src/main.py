from typing import Union

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from data.testing import dataTest

from routers import index,sso,auth,spotify
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


app.include_router(index.router)
app.include_router(sso.router)
app.include_router(auth.router)
app.include_router(spotify.router)
# @app.get("/")
# async def read_root(request:Request):
#     data=dataTest()
#     data.insertData(request.client.host)
#     return templates.TemplateResponse(
#         request=request,
#         name="index.html"
#     )


if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)