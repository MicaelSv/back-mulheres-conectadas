from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, EmailStr, ValidationError

from api import model, schema
from api.database import get_db
from api.model import Participante
from api.email_utils import send_email
from api.enums import (
    GeneroEnum,
    EtniaEnum,
    EscolaridadeEnum,
    SituacaoTrabalhoEnum,
    PresencialEnum,
    FonteProgramaEnum,
    TipoPublicacao,
)

router = APIRouter()

class EmailRequest(BaseModel):
    email: EmailStr

# Função auxiliar para transformar enums em listas de dicionários
def enum_to_dict(enum_cls):
    return [{"value": e.name, "label": e.value} for e in enum_cls]

@router.get("/inscricao_form", status_code=status.HTTP_200_OK)
def inscricao_form():
    return {
        "genero": enum_to_dict(GeneroEnum),
        "etnia": enum_to_dict(EtniaEnum),
        "escolaridade": enum_to_dict(EscolaridadeEnum),
        "situacao_trabalho": enum_to_dict(SituacaoTrabalhoEnum),
        "deseja_participar_presencial": enum_to_dict(PresencialEnum),
        "como_soube_programa": enum_to_dict(FonteProgramaEnum),
        "tipo_publicacao": enum_to_dict(TipoPublicacao),
    }

@router.post("/addUser", status_code=status.HTTP_201_CREATED)
def criar_participante(participante: schema.ParticipanteCreate, db: Session = Depends(get_db)):
    try:
        db_participante = model.Participante(**participante.dict())
        db.add(db_participante)
        db.commit()
        db.refresh(db_participante)

        subject = "Inscrição realizada com sucesso"
        body = f"""
        <html>
        <body>
            <p>Olá {db_participante.nome},</p>

            <p>Caso tenha dúvidas, você pode responder este e-mail.</p>

            <p>Atenciosamente,<br>
            Equipe Mulheres Conectadas</p>
        </body>
        </html>
        """
        send_email(db_participante.email, subject, db_participante.nome)

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Participante criado com sucesso.",
                "data": jsonable_encoder(db_participante)
            }
        )
    
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao salvar participante: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro inesperado: {str(e)}"
        )

@router.get("/users", response_model=list[schema.ParticipanteResponse], status_code=status.HTTP_200_OK)
def listar_participantes(db: Session = Depends(get_db)):
    return db.query(model.Participante).all()

@router.post("/validar_email")
async def validar_email(request: Request, db: Session = Depends(get_db)):
    body = await request.json()

    try:
        data = EmailRequest(**body)
    except ValidationError:
        return {"valid": False, "message": "Formato de e-mail inválido"}

    email_existe = db.query(Participante).filter_by(email=data.email).first()
    if email_existe:
        return {"valid": False, "message": "E-mail já cadastrado"}

    return {"valid": True}