from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from api import model, schema
from api.database import get_db
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

        subject = "Validação de Inscrição"
        body = f"""Olá {db_participante.nome}, 

        Sua inscrição foi realizada com sucesso! Para confirmar sua inscrição, clique no link abaixo:

        http://site.com/validar/{db_participante.id}

        Atenciosamente, 
        Equipe Mulheres Conectadas
        """
        send_email(db_participante.email, subject, body)
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
