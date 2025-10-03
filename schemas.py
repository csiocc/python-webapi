from pydantic import BaseModel

class PlayerBase(BaseModel):
    name: str
    email: str 
    kills: int
    wave: int
    mhscore: int = 0


class PlayerCreate(PlayerBase):
    password: str  # rohes Passwort für die Erstellung

class Player(PlayerBase):
    id: int

    class Config:
        form_attributes = True

class PlayerUpdateScore(BaseModel):
    wave: int
    kills: int

class PlayerLogin(BaseModel):
    name: str
    password: str

class PlayerUpdateMhScore(BaseModel):
    mhscore: int


