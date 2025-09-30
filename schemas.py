from pydantic import BaseModel

class PlayerBase(BaseModel):
    name: str
    kills: int
    wave: int

class PlayerCreate(PlayerBase):
    password: str  # kommt vom Client als Klartext (wird später gehasht)

class Player(PlayerBase):
    id: int

    class Config:
        form_attributes = True

class PlayerLogin(BaseModel):
    name: str
    password: str


