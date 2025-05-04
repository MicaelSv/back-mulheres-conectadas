from pydantic import BaseModel, EmailStr, AnyUrl, HttpUrl
from datetime import date, datetime
from typing import Optional
from enum import Enum

class ParticipanteBase(BaseModel):
    nome: str
    email: EmailStr
    data_nascimento: date
    genero: str
    etnia: str
    escolaridade: str
    contato: str
    situacao_trabalho: str
    rede_social: Optional[AnyUrl] = None
    cidade: str
    deseja_participar_presencial: str
    como_soube_programa: str
    autorizacao_lgpd: str

class ParticipanteCreate(ParticipanteBase):
    pass

class ParticipanteResponse(ParticipanteBase):
    id: int

    class Config:
        from_attributes = True

class TipoPublicacao(str, Enum):
    blog = "blog"
    noticia = "noticia"

class PublicacaoCreate(BaseModel):
    legenda: str
    imagem_url: HttpUrl  # ou str, caso aceite qualquer texto
    tipo: TipoPublicacao

class PublicacaoResponse(PublicacaoCreate):
    id: int
    data_publicacao: datetime

    class Config:
        from_attributes = True