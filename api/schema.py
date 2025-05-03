from pydantic import BaseModel, EmailStr, AnyUrl
from datetime import date
from typing import Optional

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
        orm_mode = True
