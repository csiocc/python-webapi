from sqlalchemy.orm import Session
import models, schemas
from utils import hash_password, verify_password
from fastapi import HTTPException

def get_players(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Player).offset(skip).limit(limit).all()

def get_player(db: Session, player_id: int):
    return db.query(models.Player).filter(models.Player.id == player_id).first()

def create_player(db: Session, player: schemas.PlayerCreate):
    # Prüfen ob Name schon existiert
    existing_name = db.query(models.Player).filter(models.Player.name == player.name).first()
    if existing_name:
        raise HTTPException(status_code=400, detail="Name already taken")

    # Prüfen ob Email schon existiert (falls Email im Schema vorhanden ist!)
    if hasattr(player, "email") and player.email:
        existing_email = db.query(models.Player).filter(models.Player.email == player.email).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(player.password)
    db_player = models.Player(
        name=player.name,
        email=player.email,   # <--- wichtig, falls im Model enthalten
        kills=player.kills,
        wave=player.wave,
        mhscore=player.mhscore,
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

# Playerscore update für Endlesswave
def update_player_score(db: Session, player_id: int, score_update: schemas.PlayerUpdateScore):
    player = db.query(models.Player).filter(models.Player.id == player_id).first()
    if not player:
        return None
    
    # Nur aktualisieren, wenn neue Werte höher sind
    if score_update.wave > player.wave:
        player.wave = score_update.wave
    if score_update.kills > player.kills:
        player.kills = score_update.kills
    
    db.commit()
    db.refresh(player)
    return player

# Playerscore update für Moorhuhnium
def update_mhscore(db: Session, player_id: int, new_score: int):
    player = db.query(models.Player).filter(models.Player.id == player_id).first()
    if not player:
        return None

    # Nur aktualisieren, wenn neue Werte höher sind
    if new_score > player.mhscore: 
        player.mhscore = new_score
        db.commit()
        db.refresh(player)

    return player
