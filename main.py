from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine

# ACHTUNG: Nur lokal verwenden!
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # für alle Origins, später einschränken
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency für DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

### ROUTEN ###

@app.post("/players/", response_model=schemas.Player, status_code=201)
def create_player(player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    existing_player = db.query(models.Player).filter(models.Player.name == player.name).first()
    if existing_player:
        raise HTTPException(status_code=400, detail="Name already exists")
    return crud.create_player(db=db, player=player)

@app.get("/players/", response_model=list[schemas.Player])
def read_players(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_players(db=db, skip=skip, limit=limit)

@app.get("/players/top10", response_model=list[schemas.Player])
def read_top10_players(db: Session = Depends(get_db)):
    return crud.get_top10_players(db)

@app.get("/players/top10/mh", response_model=list[schemas.Player])
def read_top10_mh_players(db: Session = Depends(get_db)):
    return crud.get_top10_mh_players(db)

@app.get("/players/{player_id}", response_model=schemas.Player)
def read_player(player_id: int, db: Session = Depends(get_db)):
    db_player = crud.get_player(db, player_id=player_id)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return db_player

@app.put("/players/{player_id}/score", response_model=schemas.Player)
def update_player_score(player_id: int, score_update: schemas.PlayerUpdateScore, db: Session = Depends(get_db)):
    player = crud.update_player_score(db, player_id, score_update)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

@app.put("/players/{player_id}/mhscore", response_model=schemas.Player)
def update_player_mhscore(player_id: int, score_update: schemas.PlayerUpdateMhScore, db: Session = Depends(get_db)):
    player = crud.update_player_mhscore(db, player_id, score_update.mhscore)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

@app.post("/login/", response_model=schemas.Player)
def login(player: schemas.PlayerLogin, db: Session = Depends(get_db)):
    db_player = crud.authenticate_player(db, name=player.name, password=player.password)
    if not db_player:
        raise HTTPException(status_code=401, detail="Invalid name or password")
    return db_player
