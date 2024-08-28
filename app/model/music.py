from sqlalchemy.orm import Mapped, mapped_column

from app.model.base import Base




class Music(Base):
    __tablename__ = 'Music'
    # mno : 음악번호
    mno: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    title: Mapped[str] # 제목
    singer: Mapped[str] # 가수
    year: Mapped[int] # 발매년도
    genre: Mapped[str] # 장르
    country :Mapped[str] # 국가유형 (Jpop/Kpop/Pop)
    ment: Mapped[str] # 앨범소개
    lyrics: Mapped[str] # 가사
    iname: Mapped[str] # 이미지이름
    fname: Mapped[str] # 파일이름

class MusicVideo(Base):
    __tablename__ = 'Musicvideo'
    # mno : MV번호
    mvno: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    lyrics: Mapped[str] # 가사
    iname: Mapped[str] # 이미지이름
    fname: Mapped[str] # 파일이름