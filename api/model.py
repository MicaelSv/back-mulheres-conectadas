from sqlalchemy import Column, Integer, String, Date, Text, DateTime, Enum
from database import Base
from datetime import datetime
import enum

class Participante(Base):
    __tablename__ = "participantes"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    data_nascimento = Column(Date, nullable=False)
    genero = Column(String(100), nullable=False)
    etnia = Column(String(100), nullable=False)
    escolaridade = Column(String(150), nullable=False)
    contato = Column(String(50), nullable=False)

    situacao_trabalho = Column(String(255), nullable=False)

    rede_social = Column(String(255), nullable=True)

    cidade = Column(String(255), nullable=False)

    deseja_participar_presencial = Column(String(50), nullable=False)  # sim / não / talvez
    como_soube_programa = Column(String(100), nullable=False)  # instagram, linkedin, etc

    autorizacao_lgpd = Column(Text, nullable=False)  # sim ou justificativa

class TipoPublicacao(str, enum.Enum):
    blog = "blog"
    noticia = "noticia"

class Publicacao(Base):
    __tablename__ = "publicacoes"

    id = Column(Integer, primary_key=True, index=True)
    legenda = Column(String, nullable=False)
    imagem_url = Column(String, nullable=False)
    tipo = Column(Enum(TipoPublicacao), nullable=False)
    data_publicacao = Column(DateTime, default=datetime.utcnow)
