from functools import wraps
from typing import Optional
from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
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




@router.get("/playlist",tags=[auth_required.__name__],response_class=HTMLResponse)
@auth_required
async def playlist(request:Request):
    response:Response = get("https://api.spotify.com/v1/me/playlists",
        headers={f"Authorization":f"{request.cookies.get('token_type')} {request.cookies.get('access_token')}"}
            )
    items = response.json()['items']
    
    return templates.TemplateResponse(
        request=request,
        name="components/playlists.html",
        context={"response":response.json()}
    )

@router.get("/playlist/{playlist_number}",tags=[auth_required.__name__])
@auth_required
async def playlist_number(request:Request,playlist_number:int):
    response:Response = get("https://api.spotify.com/v1/me/playlists",
        headers={f"Authorization":f"{request.cookies.get('token_type')} {request.cookies.get('access_token')}"}
            )
    items = response.json()['items'][playlist_number]
    
    tracks = items['tracks']['href']
    tracks:Response = get(tracks,
        headers={f"Authorization":f"{request.cookies.get('token_type')} {request.cookies.get('access_token')}"}
            )
    print(tracks.json())
    
    return JSONResponse(jsonable_encoder([items,tracks.json()]))




