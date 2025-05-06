from datetime import date, datetime
from pydantic import BaseModel, EmailStr, AnyUrl, HttpUrl
from typing import Optional

from api.enums import (
    GeneroEnum,
    EtniaEnum,
    EscolaridadeEnum,
    SituacaoTrabalhoEnum,
    PresencialEnum,
    FonteProgramaEnum,
    TipoPublicacao,
)

class ParticipanteBase(BaseModel):
    nome: str
    email: EmailStr
    data_nascimento: date
    genero: GeneroEnum
    etnia: EtniaEnum
    escolaridade: EscolaridadeEnum
    contato: str
    situacao_trabalho: SituacaoTrabalhoEnum
    rede_social: Optional[AnyUrl] = None
    cidade: str
    deseja_participar_presencial: PresencialEnum
    como_soube_programa: FonteProgramaEnum
    autorizacao_lgpd: str

class ParticipanteCreate(ParticipanteBase):
    pass

class ParticipanteResponse(ParticipanteBase):
    id: int

    class Config:
        from_attributes = True

class PublicacaoCreate(BaseModel):
    legenda: str
    imagem_url: HttpUrl  # ou str, caso aceite qualquer texto
    tipo: TipoPublicacao

class PublicacaoResponse(PublicacaoCreate):
    id: int
    data_publicacao: datetime

    class Config:
        from_attributes = True