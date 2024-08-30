import os
import random

import aiofiles
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse, StreamingResponse, HTMLResponse, JSONResponse, FileResponse
from starlette.templating import Jinja2Templates
from starlette.requests import Request

from app.dbfactory import get_db
from app.model.music import MusicVideo
from app.service.music import MusicService, MusicVideoService, Mp3Service

music_router= APIRouter()

templates = Jinja2Templates(directory='views/templates')

# 음악 메인페이지
@music_router.get('/index')
async def index(req: Request, db: Session = Depends(get_db)):
    try:
        mlist = MusicService.select_music(db)
        return templates.TemplateResponse('/music/index.html', {'request': req, 'mlist': mlist})
    except Exception as ex:
        print(f'▷▷▷ music_list 오류발생 : {str(ex)}')
        return RedirectResponse(url='/member/error', status_code=303)

# 장르 - dance
@music_router.get('/dance')
async def dance(req: Request, db: Session = Depends(get_db)):
    try:
        mlist = MusicService.get_music_genre(db, 'dance')
        return templates.TemplateResponse('/music/dance.html', {'request': req, 'mlist': mlist})
    except Exception as ex:
        print(f'▷▷▷ dance_list 오류발생 : {str(ex)}')
        return RedirectResponse(url='/member/error', status_code=303)

# 장르 - hiphop
@music_router.get('/hiphop')
async def hiphop(req: Request, db: Session = Depends(get_db)):
    try:
        mlist = MusicService.get_music_genre(db, 'hiphop')
        return templates.TemplateResponse('/music/hiphop.html', {'request': req, 'mlist': mlist})
    except Exception as ex:
        print(f'▷▷▷ dance_list 오류발생 : {str(ex)}')
        return RedirectResponse(url='/member/error', status_code=303)

# 장르 - ballad
@music_router.get('/ballad')
async def ballad(req: Request, db: Session = Depends(get_db)):
    try:
        mlist = MusicService.get_music_genre(db, 'ballad')
        return templates.TemplateResponse('/music/ballad.html', {'request': req, 'mlist': mlist})
    except Exception as ex:
        print(f'▷▷▷ ballad_list 오류발생 : {str(ex)}')
        return RedirectResponse(url='/member/error', status_code=303)

# 국가별 - kpop
@music_router.get('/kpop')
async def kpop(req: Request, db: Session = Depends(get_db)):
    try:
        mlist = MusicService.get_music_country(db, 'kpop')
        return templates.TemplateResponse('/music/kpop.html', {'request': req, 'mlist': mlist})
    except Exception as ex:
        print(f'▷▷▷ kpop_list 오류발생 : {str(ex)}')
        return RedirectResponse(url='/member/error', status_code=303)

# 국가별 - jpop
@music_router.get('/jpop')
async def jpop(req: Request, db: Session = Depends(get_db)):
    try:
        mlist = MusicService.get_music_country(db, 'jpop')
        return templates.TemplateResponse('/music/jpop.html', {'request': req, 'mlist': mlist})
    except Exception as ex:
        print(f'▷▷▷ jpop_list 오류발생 : {str(ex)}')
        return RedirectResponse(url='/member/error', status_code=303)

# 국가별 - pop
@music_router.get('/pop')
async def kpop(req: Request, db: Session = Depends(get_db)):
    try:
        mlist = MusicService.get_music_country(db, 'pop')
        return templates.TemplateResponse('/music/pop.html', {'request': req, 'mlist': mlist})
    except Exception as ex:
        print(f'▷▷▷ pop_list 오류발생 : {str(ex)}')
        return RedirectResponse(url='/member/error', status_code=303)

# 제목 or 가수로 검색
@music_router.get('/search')
async def search(req: Request, query: str = '',db: Session = Depends(get_db)):
    try:
        mlist = MusicService.get_music_search(db, title=query, singer=query)
        return templates.TemplateResponse('/music/search.html', {'request': req, 'mlist': mlist})
    except Exception as ex:
        print(f'▷▷▷ search 오류발생 : {str(ex)}')
        return RedirectResponse(url='/member/error', status_code=303)

@music_router.get('/music')
async def music(req: Request):
    return templates.TemplateResponse('/music/music.html', {'request': req})

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
async def mp3play(mno: int, db: Session = Depends(get_db) ):

    MUSIC_PATH = 'd:/test/music/'
    music_fname = Mp3Service.music_mp3(db, mno)

    file_path = os.path.join(MUSIC_PATH, music_fname)

    async def iterfile():
        async with aiofiles.open(file_path, 'rb') as f:
            while chunk := await f.read(64 * 1024):
                yield chunk

    return StreamingResponse(iterfile(),media_type='audio/mp3')

# 뮤직 이미지
@music_router.get('/musiccover/{mno}', response_class=HTMLResponse)
async def musiccover(mno: int, db: Session = Depends(get_db) ):

    MUSICIMAGE_PATH = 'd:/test/musicimage/'
    mp3_image = Mp3Service.selectone_musicimage(db, mno)

    file_path = os.path.join(MUSICIMAGE_PATH, mp3_image )

    return FileResponse(file_path, media_type='image/jpeg')

# 뮤직비디오,랜덤
@music_router.get('/random_mvno', response_class=JSONResponse)
async def random_mvno(db: Session = Depends(get_db)):
    mvno = MusicVideoService.get_random_mvno(db)
    if mvno is None:
        return JSONResponse(content={"error": "No music videos available"}, status_code=404)
    return JSONResponse(content={"mvno": mvno})

@music_router.get('/mp4play/{mvno}', response_class=HTMLResponse)
async def mp4play(mvno: int, db: Session = Depends(get_db) ):

    MV_PATH = 'd:/test/mv/'
    mv_fname = MusicVideoService.selectone_file(db, mvno)

    file_path = os.path.join(MV_PATH, mv_fname)

    async def iterfile():
        async with aiofiles.open(file_path, 'rb') as f:
            while chunk := await f.read(64 * 1024):
                yield chunk

    return StreamingResponse(iterfile(), media_type='video/mp4')
# 뮤비 커버이미지
@music_router.get('/mvcover/{mvno}', response_class=HTMLResponse)
async def mvcover(mvno: int, db: Session = Depends(get_db) ):

    IMAGE_PATH = 'd:/test/mvimage/'
    mv_image = MusicVideoService.selectone_mvimage(db, mvno)

    file_path = os.path.join(IMAGE_PATH, mv_image )

    return FileResponse(file_path, media_type='image/jpeg')
# 뮤비 가사
@music_router.get('/mvlyrics/{mvno}', response_class=HTMLResponse)
async def mvlyrics(mvno: int, db: Session = Depends(get_db) ):

    mv_lyrics = MusicVideoService.selectone_mvlyrics(db, mvno)

    file_path = os.path.join(mv_lyrics)

    return HTMLResponse(content=file_path, media_type='text/html')

@music_router.get('/random_mvnos', response_class=JSONResponse)
async def random_mvnos(db: Session = Depends(get_db)):
    # Get all mvno values
    stmt = select(MusicVideo.mvno)
    results = db.execute(stmt).scalars().all()

    # Check if we have enough data
    if not results or len(results) < 3:
        return JSONResponse(content={"error": "Not enough music videos available"}, status_code=404)

    # Randomly select 3 unique mvno values
    random_mvnos = random.sample(results, 3)

    return JSONResponse(content={"mvnos": random_mvnos})

# FastAPI 엔드포인트에서 호출
@music_router.get('/music/index')
async def index(db: Session = Depends(get_db)):
    music_list = MusicService.get_random_music_list(db)
    return {"mlist": music_list}