from functools import wraps
from typing import Optional
from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response
from .auth import auth_required
from data.testing import dataTest
from pydantic import BaseModel, Field
from dotenv import load_dotenv,find_dotenv
from requests import post,get
router = APIRouter(
    prefix="/spotify",
    tags=["Spotify Frontend API"]
    
)

templates = Jinja2Templates(directory="templates")
load_dotenv(find_dotenv())

@router.get("/playlist",tags=[auth_required.__name__])
@auth_required
async def playlists(request:Request):
    response:Response = get("https://api.spotify.com/v1/me/playlists",
        headers={f"Authorization":f"{request.cookies.get('token_type')} {request.cookies.get('access_token')}"}
            )
    return response.json()





