from typing import Optional
from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, RedirectResponse, Response
from ..data.testing import dataTest
from pydantic import BaseModel, Field, field_validator, validator
import os
from dotenv import load_dotenv,find_dotenv
from requests import post
import base64
router = APIRouter(
    prefix="/sso"
)
templates = Jinja2Templates(directory="templates")
load_dotenv(find_dotenv())

class URL:
    url = "http://127.0.0.1:8000"
    @classmethod
    def get_url(self):
        return self.url;
    @classmethod
    def set_url(self,url):
        self.url = url;

class SpotifyAuth(BaseModel):

   
    response_type:str = 'code'
    client_id:str = os.environ.get("CLIENT_ID")
    scope:str = "user-read-private user-read-email playlist-read-private playlist-read-collaborative"
    redirect_uri:Optional[str] = URL.get_url()


    class Config:
        validate_assignment = True
    
    
class SpotifyCallback(BaseModel):
    code:str
    state:Optional[str] = Field(None,description="state of spotify request")
class SpotifyAuthResponse(BaseModel):
    access_token:str
    token_type:str
    scope:str
    expires_in:int
    refresh_token:str
@router.get("/spotify")
async def spotify(request:Request, model:SpotifyAuth = Depends()):
    prod_or_no =os.environ.get("PROD")
    print(f"{prod_or_no=}")
    if (os.environ.get("PROD")=="True"):
        URL.set_url(str(request.url).replace("http","https") + "/callback") 
    else:
        URL.set_url( str(request.url) + "/callback")

    return RedirectResponse(f"https://accounts.spotify.com/authorize?response_type={model.response_type}&client_id={model.client_id}&scope={model.scope}&redirect_uri={URL.get_url()}")


@router.get("/spotify/callback")
def spotify_callback(request:Request,model:SpotifyCallback = Depends()):
    print(f"{request.query_params=}")
    auth = base64.b64encode(f"{ os.environ.get('CLIENT_ID')}:{ os.environ.get('CLIENT_SECRET')}".encode("utf-8")).decode("ascii")
    
    value:Response = post(
        url="https://accounts.spotify.com/api/token",
        data= {
            "code": model.code,
            "redirect_uri":URL.get_url(),
            "grant_type": 'authorization_code',
        },
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
                    'Authorization': f"Basic {auth}"
        }
    )
    print(f"{value.json()=}")
    dictionay = dict(value.json())
    models:SpotifyAuthResponse = SpotifyAuthResponse(**dictionay)
    redirect_url = request.url_for("read_root")
    print(f"{redirect_url=}")
    response = RedirectResponse(redirect_url)
    
    response.set_cookie("access_token",models.access_token)
    response.set_cookie("token_type",models.token_type)
    response.set_cookie("expires_in",models.expires_in)

    
    return response
        
    



