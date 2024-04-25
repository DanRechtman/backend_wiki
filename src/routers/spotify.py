from functools import wraps
import json
import time
from typing import List, Optional, Union
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
class Added_By(BaseModel):
    external_urls: Optional[ExternalUrls]=None
    followers: Optional[Followers]=None
    href:Optional[str] = None
    id:Optional[str] = None
    type:Optional[str] = None
    uri:Optional[str] = None


class Restrictions(BaseModel):
    reason:Optional[str]=None

class SimplifiedArtistObject(BaseModel):
    external_urls:Optional[ExternalUrls]=None
    href:Optional[str] = None
    id:Optional[str] = None
    name:Optional[str] = None
    type:Optional[str] = None
    uri:Optional[str] = None
class Album(BaseModel):
    album_type:Optional[str] = None
    total_track:Optional[str] = None
    available_markets:list[str]
    external_urls: Optional[ExternalUrls]=None
    href:Optional[str] = None
    id:Optional[str] = None
    images:list[ImageObjects]
    name:Optional[str] = None
    release_date:Optional[str] = None
    release_date_precision:Optional[str] = None
    restrictions:Optional[Restrictions]=None
    type:Optional[str] = None
    uri:Optional[str] = None
    artists:Optional[list[SimplifiedArtistObject]]=None

class ArtistObject(BaseModel):
    external_urls:Optional[ExternalUrls]=None
    followers:Optional[Followers]=None
    genres:Optional[list[str]]=None
    href:Optional[str]=None
    id:Optional[str]=None
    images:Optional[list[ImageObjects]]=None
    name:Optional[str]=None
    popularity:Optional[int]=None
    type:Optional[str]=None
    uri:Optional[str]=None

class ExternalIds(BaseModel):
    isrc:Optional[str]=None
    ean:Optional[str]=None
    upc:Optional[str]=None
class TrackObject(BaseModel):
    album: Optional[Album]=None
    artists:Optional[list[ArtistObject]]=None
    available_markets:Optional[list[str]]=None
    disc_number:Optional[int]=None
    duration_ms:Optional[int]=None
    explicit:Optional[bool]=None
    external_ids:Optional[ExternalIds]=None
    external_urls:Optional[ExternalUrls]=None
    href:Optional[str] = None
    id:Optional[str]=None
    is_playable:Optional[bool]=None
    linked_from:Optional[str]=None
    restrictions:Optional[Restrictions]=None
    name:Optional[str] = None
    popularity:Optional[int]=None
    preview_url:Optional[str] = None
    track_number:Optional[int]=None
    type:Optional[str] = None
    uri:Optional[str] = None
    is_local:bool

class ResumePoint(BaseModel):
    fully_played:bool
    resume_position_ms:int

class CopyrightObjects(BaseModel):
    text:str
    type:str
class Show(BaseModel):
    available_markets:list[str]
    copyrights:list[CopyrightObjects]
    description:Optional[str] = None
    html_description:Optional[str] = None
    explicit:bool
    external_urls:ExternalUrls
    href:Optional[str] = None
    id:Optional[str] = None
    images:list[ImageObjects]
    is_externally_hosted:bool
    language:list[str]
    media_type:Optional[str] = None
    name:Optional[str] = None
    publisher:Optional[str] = None
    type:Optional[str] = None
    uri:Optional[str] = None
    total_episodes:Optional[int] = None

class EpisodeObject(BaseModel):
    audio_preview_url:Optional[str] = None
    description:Optional[str] = None
    html_description:Optional[str] = None
    duration_ms:Optional[int]=None
    explicit:Optional[bool]=None
    external_urls:Optional[ExternalUrls]=None
    href:Optional[str] = None
    id:Optional[str] = None
    images:Optional[list[ImageObjects]]=None
    is_externally_hosted:Optional[bool]=None
    is_playable:Optional[bool]=None
    language:Optional[str] = None
    languages:Optional[list[str]]=None
    name:Optional[str] = None
    release_date:Optional[str] = None
    release_date_precision:Optional[str] = None
    resume_point:Optional[ResumePoint]=None
    type:Optional[str] = None
    uri:Optional[str] = None
    restrictions:Optional[Restrictions]=None
    show: Optional[Show]=None
class PlaylistTrackObject(BaseModel):
    added_at:Optional[str]=None
    added_by:Optional[Added_By]=None
    is_local:Optional[bool]=None
    track: Optional[Union[TrackObject,EpisodeObject]]=None
class Track(BaseModel):
    href:Optional[str]=None
    limit:Optional[int] = None
    next:Optional[str] = None
    offset:Optional[int] =None
    previous:Optional[str] = None
    total:Optional[int]=None
    items:Optional[list[PlaylistTrackObject]]=None
class Playlist(BaseModel):
    collaborative:bool = None
    description:Optional[str] = None
    external_urls:Optional[ExternalUrls] = None
    followers:Optional[Followers] = None
    href:Optional[str] = None
    id:Optional[str] = None
    images:Optional[list[ImageObjects]] = None
    name:Optional[str] = None
    owner:Optional[Owner] = None
    public:Optional[bool] = None
    snapshot_id:Optional[str] = None
    tracks:Optional[Track] = None
    type:Optional[str] = None
    uri:Optional[str]=None

@router.get("/playlist",tags=[auth_required.__name__],response_class=HTMLResponse)
@auth_required
async def playlist(request:Request):
    response:Response = get("https://api.spotify.com/v1/me/playlists",
        headers={f"Authorization":f"{request.cookies.get('token_type')} {request.cookies.get('access_token')}"}
            )
    playlist:PlaylistCurrentUser = PlaylistCurrentUser().model_validate_json(response.text)
    
    return templates.TemplateResponse(
        request=request,
        name="components/playlists.html",
        context={"response":playlist.items}
    )

# @router.get("/playlist/{playlist_number}",tags=[auth_required.__name__])
# @auth_required
# async def playlist_number(request:Request,playlist_number:int):
#     response = get("https://api.spotify.com/v1/me/playlists",
#         headers={f"Authorization":f"{request.cookies.get('token_type')} {request.cookies.get('access_token')}"}
#             )
#     playlist:PlaylistCurrentUser = PlaylistCurrentUser().model_validate_json(response.text)
 
#     for i in playlist.items:
#         print(f"{i.owner}")
#         print(f"{i.name}")

#     return JSONResponse( playlist.items[0].name )

def HelperMethod(request,playlist:str)->list:
    
    if (playlist is None):
        return []
    response = get(playlist+"/tracks",
                    headers={f"Authorization":f"{request.cookies.get('token_type')} {request.cookies.get('access_token')}"})

    playlist_obj:Track = Track(**response.json())
        
    arr = []
    for track in playlist_obj.tracks.items:
        arr.append([track.track.name, track.track.popularity])
    return arr + HelperMethod(request,playlist_obj.tracks.next)

@router.get("/playlist/{playlist_id}",tags=[auth_required.__name__])
@auth_required
async def tracks(request:Request, playlist_id):

    response = get(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
                   headers={f"Authorization":f"{request.cookies.get('token_type')} {request.cookies.get('access_token')}"})
    playlist:Track = Track(**response.json())
    arr = []

    response.close()

    for track in playlist.items:
        arr.append([track.track.name, [artist.name for artist in track.track.artists],track.track.id,track.track.album.images])
    offset = 100
    while (playlist.total >= offset):
        response = get(playlist.next,
                   headers={"Authorization":f"{request.cookies.get('token_type')} {request.cookies.get('access_token')}",
                            'Cache-Control': 'no-cache',
                            "Pragma": "no-cache"
                            },
                   )
        
        playlist:Track = Track(**response.json())
        
        for track in playlist.items:
            arr.append([track.track.name, [artist.name for artist in track.track.artists],track.track.id,track.track.album.images])
        offset+=100
    return templates.TemplateResponse(
        request=request,
        name="MoreDetailsPlaylist.html",
        context={"arr":arr}
    )
    
    

