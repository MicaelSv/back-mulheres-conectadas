from database import Base, engine
from model import Participante

Base.metadata.create_all(bind=engine)
