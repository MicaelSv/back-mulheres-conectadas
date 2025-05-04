from api.database import Base, engine
from api.model import Participante, Publicacao

Base.metadata.drop_all(bind=engine)  # Apaga tudo
Base.metadata.create_all(bind=engine)  # Cria tudo do zero
