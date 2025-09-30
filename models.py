from sqlalchemy import Column, Integer, String
from database import Base

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    kills = Column(Integer, default=0)
    wave = Column(Integer, default=1)
    password_hash = Column(String)  # hier wird das gehashte Passwort gespeichert
