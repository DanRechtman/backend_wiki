from functools import wraps
from typing import Optional
from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response
from data.testing import dataTest
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv,find_dotenv
from requests import post,get
import base64
router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
    
)

# Decorator
def auth_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        print(f"{kwargs=}")
        request = kwargs['request']
        authed = await logged(request=request)
        print(f"{authed=}")
        if (authed):
            return await func(*args,**kwargs)
        else:
            return HTMLResponse("Please Authenticate")
    return wrapper


templates = Jinja2Templates(directory="templates")
load_dotenv(find_dotenv())

@router.get("/me")
@auth_required
async def me(request:Request):
    response:Response = get("https://api.spotify.com/v1/me",
        headers={f"Authorization":f"{request.cookies.get('token_type')} {request.cookies.get('access_token')}"}
            )
    return response.json()


@router.get('/logged',description="Check if user is logged in")
async def logged(request:Request)->bool:
    response:Response = get("https://api.spotify.com/v1/me",
        headers={f"Authorization":f"{request.cookies.get('token_type')} {request.cookies.get('access_token')}"}
            )
    authed = False
    print(response)
    if 'error' in response.json():
        authed =False
    else:
        authed = True

    return authed
    





