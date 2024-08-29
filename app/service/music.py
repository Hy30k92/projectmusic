import random

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.model.music import Music
from app.model.music import MusicVideo

class MusicService:
    @staticmethod
    def select_music(db):
        try:
            # 페이지당 항목 수
            items_per_page = 10

            # SQL 쿼리 작성
            stmt = select(Music.mno,Music.singer, Music.title).limit(items_per_page)

            # 쿼리 실행 및 결과 반환
            result = db.execute(stmt)
            return result.fetchall()  # Row 객체의 리스트를 반환

        except SQLAlchemyError as ex:
            print(f'▶▶▶ select_music 오류발생 : {str(ex)}')
            return []

class Mp3Service:
    @staticmethod
    def music_mp3(db, mno):
        try:
            find_pno = Music.mno == mno
            stmt = select(Music.fname).where(find_pno)
            result = db.execute(stmt).scalars().first()

            return result

        except SQLAlchemyError as ex:
            print(f'▶▶▶  music_mp3 오류 발생: , {str(ex)}')
            
class MusicVideoService:
    @staticmethod
    def selectone_file(db, mvno):
        try:
            # stmt = (select(MusicVideo.fname,MusicVideo.lyrics,MusicVideo.iname)\
            #         .where(MusicVideo.mvno == mvno))
            stmt = select(MusicVideo.fname).where(MusicVideo.mvno == mvno)
            result = db.execute(stmt).scalars().first()
            return result

        except SQLAlchemyError as ex:
            print(f'▶▶▶ selectone_file 오류 발생 : {str(ex)}')

    @staticmethod
    def selectone_mvimage(db, mvno):
        try:
            stmt = select(MusicVideo.iname).where(MusicVideo.mvno == mvno)
            result = db.execute(stmt).scalars().first()
            return result

        except SQLAlchemyError as ex:
            print(f'▶▶▶ selectone_file 오류 발생 : {str(ex)}')

    @staticmethod
    def selectone_mvlyrics(db, mvno):
        try:
            stmt = select(MusicVideo.lyrics).where(MusicVideo.mvno == mvno)
            result = db.execute(stmt).scalars().first()
            return result

        except SQLAlchemyError as ex:
            print(f'▶▶▶ selectone_file 오류 발생 : {str(ex)}')

    @staticmethod
    def get_random_mvno(db: Session):
        stmt = select(MusicVideo.mvno)  # Query all mvno values
        results = db.execute(stmt).scalars().all()  # Fetch all results
        return random.choice(results) if results else None  # Choose randomly



