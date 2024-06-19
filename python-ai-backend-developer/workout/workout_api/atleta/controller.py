from fastapi import APIRouter, Body, HTTPException, status, Depends, FastAPI
from fastapi_pagination import Page, Params, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate as paginate_sqlalchemy
from pydantic import UUID4
from uuid import uuid4
from datetime import datetime
from sqlalchemy import join
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from workout_api.atleta.models import AtletaModel
from workout_api.atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate, AtletaResumo
from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.contrib.dependencies import DataBaseDependency

router = APIRouter()
app = FastAPI()
add_pagination(app)
app.include_router(router)

@router.post(
    '/',
    summary='Criar um novo atleta',
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut
)
async def post(
        db_session: DataBaseDependency,
        atleta_in: AtletaIn = Body(...)
):
    categoria_nome = atleta_in.categoria.nome
    centro_treinamento_nome = atleta_in.centro_treinamento.nome

    categoria = (await db_session.execute(
        select(CategoriaModel).filter_by(nome=categoria_nome))
                 ).scalars().first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'A categoria {categoria_nome} não foi encontrada.'
        )

    centro_treinamento = (await db_session.execute(
        select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome))
                          ).scalars().first()

    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'O centro de treinamento {centro_treinamento_nome} não foi encontrado.'
        )
    try:
        atleta_out = AtletaOut(id=uuid4(), created_at=datetime.utcnow(), **atleta_in.model_dump())
        atleta_model = AtletaModel(**atleta_out.model_dump(exclude={'categoria', 'centro_treinamento'}))

        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id

        db_session.add(atleta_model)
        await db_session.commit()

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f'Já existe um atleta cadastrado com o cpf: {atleta_in.cpf}.'
        )
        db_session.rollback()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Ocorreu um erro ao inserir os dados no banco: {e}'
        )

    return atleta_out

@router.get(path='/',
             summary='Obter todos os atletas'
             , status_code=status.HTTP_200_OK
             , response_model=list[AtletaOut])
async def get_all(db_session: DataBaseDependency, nome: Optional[str] = None, cpf: Optional[str] = None) -> (
        list)[AtletaOut]:
    query = select(AtletaModel)

    if nome:
        query = query.filter(AtletaModel.nome == nome)

    if cpf:
        query = query.filter(AtletaModel.cpf == cpf)

    atletas: list[AtletaOut] = (await db_session.execute(query)).scalars().all()
    return atletas

@router.get(path='/paginate',
             summary='Obter todos os atletas com paginação'
             , status_code=status.HTTP_200_OK
             , response_model=Page[AtletaOut])
async def get_atletas(db_session: DataBaseDependency, params: Params = Depends()) -> Page[AtletaOut]:
    atletas = select(AtletaModel).order_by(AtletaModel.created_at)
    return await paginate_sqlalchemy(db_session, atletas, params)

@router.get(path='/resumo',
             summary='Obter todos os atletas com response personalizado'
             , status_code=status.HTTP_200_OK
             , response_model=list[AtletaResumo])
async def get_all_resumo(db_session: DataBaseDependency) -> (
        list)[AtletaResumo]:
    query = select(AtletaModel.nome, CentroTreinamentoModel.nome.label("centro_treinamento"),
                   CategoriaModel.nome.label("categoria"))
    query = query.select_from(AtletaModel)
    query = query.join(CentroTreinamentoModel, AtletaModel.centro_treinamento_id == CentroTreinamentoModel.pk_id)
    query = query.join(CategoriaModel, AtletaModel.categoria_id == CategoriaModel.pk_id)

    result = await db_session.execute(query)
    atletas = [AtletaResumo(nome=row[0], centro_treinamento=row[1], categoria=row[2]) for row in result]

    return atletas

@router.get(path='/{id}',
             summary='Obter atleta por Id'
             , status_code=status.HTTP_200_OK
             , response_model=AtletaOut)
async def query(id: UUID4, db_session: DataBaseDependency) -> AtletaOut:
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
            , detail='Atleta não encontrado'
        )

    return atleta


@router.patch(
    '/{id}',
    summary='Editar um atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def patch(id: UUID4, db_session: DataBaseDependency, atleta_up: AtletaUpdate = Body(...)) -> AtletaOut:
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrado no id: {id}'
        )

    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update.items():
        setattr(atleta, key, value)

    await db_session.commit()
    await db_session.refresh(atleta)

    return atleta

@router.delete(
    '/{id}',
    summary='Deletar um Atleta pelo id',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete(id: UUID4, db_session: DataBaseDependency) -> None:
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrado no id: {id}'
        )

    await db_session.delete(atleta)
    await db_session.commit()