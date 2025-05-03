from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import model, schema
from database import SessionLocal, engine

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependência para abrir sessão com o banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/addUser", response_model=schema.ParticipanteResponse)
def criar_participante(participante: schema.ParticipanteCreate, db: Session = Depends(get_db)):
    db_participante = model.Participante(**participante.dict())
    db.add(db_participante)
    db.commit()
    db.refresh(db_participante)
    return db_participante

@app.get("/users", response_model=list[schema.ParticipanteResponse])
def listar_participantes(db: Session = Depends(get_db)):
    return db.query(model.Participante).all()
