from api.database import Base, engine
from api.model import Participante, Publicacao

Base.metadata.create_all(bind=engine)
