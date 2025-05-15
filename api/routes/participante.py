from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, EmailStr, ValidationError
from sqlalchemy import func

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

ADMIN_USERS = {
    "gesyca@admin.com": {"senha": "senhaGesyca123", "nome": "Gesyca"},
    "alessandra@admin.com": {"senha": "senhaAlessandra123", "nome": "Alessandra"},
}

class AdminLoginRequest(BaseModel):
    email: EmailStr
    senha: str

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


@router.post("/admin/login")
def login_admin(admin: AdminLoginRequest):
    user = ADMIN_USERS.get(admin.email)
    if user and admin.senha == user["senha"]:
        return {"nome": user["nome"]}
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas"
    )

@router.get("/inscricoes/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    # 1. Inscrições por cidade - Pizza
    por_cidade = (
        db.query(Participante.cidade, func.count().label("total"))
        .group_by(Participante.cidade)
        .all()
    )

    # 2. Escolaridade dos inscritos - Bar chart
    por_escolaridade = (
        db.query(Participante.escolaridade, func.count().label("total"))
        .group_by(Participante.escolaridade)
        .all()
    )

    # 3. Situação de trabalho atual - Horizontal bar chart
    por_situacao_trabalho = (
        db.query(Participante.situacao_trabalho, func.count().label("total"))
        .group_by(Participante.situacao_trabalho)
        .all()
    )


    # Organizando os dados em dicionários/arrays para facilitar o uso no front
    return {
        "por_cidade": {
            "labels": [c for c, _ in por_cidade],
            "data": [t for _, t in por_cidade]
        },
        "por_escolaridade": {
            "labels": [e for e, _ in por_escolaridade],
            "data": [t for _, t in por_escolaridade]
        },
        "por_situacao_trabalho": {
            "labels": [s for s, _ in por_situacao_trabalho],
            "data": [t for _, t in por_situacao_trabalho]
        }
    }   


@router.get("/escolaridade_por_etnia") # Group bar chart
def escolaridade_por_etnia(db: Session = Depends(get_db)):
    resultados = (
        db.query(model.Participante.etnia, model.Participante.escolaridade, func.count())
        .group_by(model.Participante.etnia, model.Participante.escolaridade)
        .all()
    )
    
    # Preparar listas únicas
    etnias = sorted(list({r[0] for r in resultados}))
    escolaridades = sorted(list({r[1] for r in resultados}))

    # Inicializar estrutura de dados
    data_map = {e: {es: 0 for es in escolaridades} for e in etnias}

    # Preencher contagens
    for etnia, escolaridade, count in resultados:
        data_map[etnia][escolaridade] = count

    # Formatar em datasets
    datasets = []
    for escolaridade in escolaridades:
        datasets.append({
            "label": escolaridade,
            "data": [data_map[etnia][escolaridade] for etnia in etnias]
        })

    return {
        "labels": etnias,
        "datasets": datasets
    }


from api.enums import PresencialEnum

@router.get("/presencial_top_cidades") # Stacked Bar Chart
def presencial_top_cidades(db: Session = Depends(get_db)):
    # 1. Top 3 cidades com mais inscritos
    subquery = (
        db.query(model.Participante.cidade)
        .group_by(model.Participante.cidade)
        .order_by(func.count().desc())
        .limit(3)
        .subquery()
    )

    # 2. Consulta: cidade x deseja_participar_presencial
    resultados = (
        db.query(
            model.Participante.cidade,
            model.Participante.deseja_participar_presencial,
            func.count()
        )
        .filter(model.Participante.cidade.in_(subquery))
        .group_by(
            model.Participante.cidade,
            model.Participante.deseja_participar_presencial
        )
        .all()
    )

    cidades = sorted(list({r[0] for r in resultados}))
    opcoes_presencial = [e.value for e in PresencialEnum]  # ['Sim', 'Não', 'Talvez']

    # Inicializa estrutura
    data_map = {
        cidade: {opcao: 0 for opcao in opcoes_presencial}
        for cidade in cidades
    }

    for cidade, deseja_presencial, count in resultados:
        data_map[cidade][deseja_presencial] = count

    # Gera datasets para o gráfico
    datasets = []
    for opcao in opcoes_presencial:
        datasets.append({
            "label": opcao,
            "data": [data_map[cidade][opcao] for cidade in cidades]
        })

    return {
        "labels": cidades,
        "datasets": datasets
    }



