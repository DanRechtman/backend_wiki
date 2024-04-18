from functools import wraps
from typing import List, Optional
from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response
from pydantic_core import from_json
from .auth import auth_required
from ..data.testing import dataTest
from pydantic import BaseModel, Field
from dotenv import load_dotenv,find_dotenv
from requests import post,get
router = APIRouter(
    prefix="/spotify",
    tags=["Spotify Frontend API"]
    
)

templates = Jinja2Templates(directory="templates")
load_dotenv(find_dotenv())

class ExternalUrls(BaseModel):
    spotify:str

class ImageObjects(BaseModel):
    url:Optional[str] = None
    height:Optional[int] = None
    width:Optional[int] = None
class Followers(BaseModel):
    href:Optional[str] = None
    total:int
class Owner(BaseModel):
    external_urls:ExternalUrls
    followers:Optional[Followers] = None
    href:str
    id: str
    type:str
    uri:str
    display_name:Optional[str] = None


class Tracks(BaseModel):
    href:str
    total:int
class SimplifiedPlaylistObject(BaseModel):
    collaborative:bool
    description:str
    external_urls:ExternalUrls
    href:str
    id:str
    images:list[ImageObjects]
    name:str
    owner:Owner
    public:bool
    snapshot_id:str
    tracks: Tracks
    type:str
    uri:str

class PlaylistCurrentUser(BaseModel):
    href:Optional[str] = None
    limit:Optional[int] = None
    next:Optional[str] = None
    offset:Optional[int] = None
    previous:Optional[str] = None
    total:Optional[int]= None
    items:Optional[list[SimplifiedPlaylistObject]] = None



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
    response = get("https://api.spotify.com/v1/me/playlists",
        headers={f"Authorization":f"{request.cookies.get('token_type')} {request.cookies.get('access_token')}"}
            )
    
    playlist:PlaylistCurrentUser = PlaylistCurrentUser().model_validate_json(response.text)
    for i in playlist.items:
        print(f"{i.owner}")
        print(f"{i.name}")

    return JSONResponse( playlist.items[0].name )




