from api.database import Base, engine
from api.model import Participante

Base.metadata.create_all(bind=engine)
