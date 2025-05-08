from fastapi import FastAPI

from .database import engine, Base
from api.routes import participante, publicacao

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(participantes.router, prefix="/participantes", tags=["Participantes"])
app.include_router(publicacao.router, prefix="/publicacoes", tags=["Publicações"])
