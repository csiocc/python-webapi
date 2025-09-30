from sqlalchemy.orm import Session
import models, schemas
from utils import hash_password
from utils import verify_password

def get_players(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Player).offset(skip).limit(limit).all()

def get_player(db: Session, player_id: int):
    return db.query(models.Player).filter(models.Player.id == player_id).first()

def create_player(db: Session, player: schemas.PlayerCreate):
    hashed_pw = hash_password(player.password)
    db_player = models.Player(
        name=player.name,
        kills=player.kills,
        wave=player.wave,
        password_hash=hashed_pw
    )
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player
    
def authenticate_player(db: Session, name: str, password: str):
    player = db.query(models.Player).filter(models.Player.name == name).first()
    if not player:
        return None
    if not verify_password(password, player.password_hash):
        return None
    return player

def get_top10_players(db: Session):
    return (
        db.query(models.Player)
        .order_by(models.Player.wave.desc(), models.Player.kills.desc())
        .limit(10)
        .all()
    )