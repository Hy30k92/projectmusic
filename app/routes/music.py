import os

import aiofiles
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse, StreamingResponse, HTMLResponse
from starlette.templating import Jinja2Templates
from starlette.requests import Request

from app.dbfactory import get_db
from app.service.music import MusicService
from app.service.music import PdsService

music_router= APIRouter()

templates = Jinja2Templates(directory='views/templates')


@music_router.get('/index')
async def index(req: Request, db: Session = Depends(get_db)):
    try:
        mlist = MusicService.select_music(db)
        return templates.TemplateResponse('/music/index.html', {'request': req, 'mlist': mlist})
    except Exception as ex:
        print(f'▷▷▷ music_list 오류발생 : {str(ex)}')
        return RedirectResponse(url='/member/error', status_code=303)


@music_router.get('/music')
async def music(req: Request):
    return templates.TemplateResponse('music/music.html', {'request': req})

@music_router.get('/musicvideo')
async def musicvideo(req: Request):
    return templates.TemplateResponse('music/musicvideo.html', {'request': req})

@music_router.get('/storage')
async def storage(req: Request):
    return templates.TemplateResponse('music/storage.html', {'request': req})

@music_router.get('/test')
async def test(req: Request):
    return templates.TemplateResponse('music/test.html', {'request': req})

# 음악 플레이
@music_router.get('/mp3play/{mno}', response_class=HTMLResponse)
async def mp3play(mno:int,db:Session = Depends(get_db) ):

    MUSIC_PATH = 'C:/java/pdsupload/music/'
    audio_fname = PdsService.music_mp3(db, mno)
    file_path = os.path.join(MUSIC_PATH, audio_fname)

    async def iterfile():
        async with aiofiles.open(file_path, 'rb') as f:
            while chunk := await f.read(64 * 1024): # 64k chunk
                yield  chunk

    return StreamingResponse(iterfile(),media_type='audio/mp3')