from fastapi import APIRouter, Body, HTTPException, status, Depends, FastAPI
from fastapi_pagination import Page, Params, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate as paginate_sqlalchemy
from pydantic import UUID4
from uuid import uuid4
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from workout_api.contrib.dependencies import DataBaseDependency
from workout_api.centro_treinamento.schemas import CentroTreinamentoIn, CentroTreinamentoOut
from workout_api.centro_treinamento.models import CentroTreinamentoModel

router = APIRouter()
app = FastAPI()
add_pagination(app)
app.include_router(router)

@router.post(path='/',
             summary='Criar novo centro de treinamento'
             , status_code=status.HTTP_201_CREATED
             , response_model=CentroTreinamentoOut)
async def post(
           db_session: DataBaseDependency,
           centro_treinamento_in: CentroTreinamentoIn = Body(...)
    ) -> CentroTreinamentoOut:

    try:
        centro_treinamento_out = CentroTreinamentoOut(id=uuid4(), **centro_treinamento_in.model_dump())
        centro_treinamento_model = CentroTreinamentoModel(**centro_treinamento_out.model_dump())
        db_session.add(centro_treinamento_model)
        await db_session.commit()

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f'Já existe um centro de treinamento com o nome: {centro_treinamento_in.nome}.'
        )
        db_session.rollback()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Ocorreu um erro ao inserir os dados no banco: {e}'
        )
        db_session.rollback()

    return centro_treinamento_out


@router.get(path='/',
             summary='Obter todos os centros de treinamento'
             , status_code=status.HTTP_200_OK
             , response_model=list[CentroTreinamentoOut])
async def query(db_session: DataBaseDependency) -> list[CentroTreinamentoOut]:
    centros_treinamento: list[CentroTreinamentoOut] = (await db_session.execute(select(CentroTreinamentoModel))
                                      ).scalars().all()
    return centros_treinamento

@router.get(path='/paginate',
             summary='Obter todos os centros de treinamento com paginação'
             , status_code=status.HTTP_200_OK
             , response_model=Page[CentroTreinamentoOut])
async def get_cts(db_session: DataBaseDependency, params: Params = Depends()) -> Page[CentroTreinamentoOut]:
    cts = select(CentroTreinamentoModel).order_by(CentroTreinamentoModel.nome)
    return await paginate_sqlalchemy(db_session, cts, params)

@router.get(path='/{id}',
             summary='Obter centro de treinamento por Id'
             , status_code=status.HTTP_200_OK
             , response_model=CentroTreinamentoOut)
async def query(id: UUID4, db_session: DataBaseDependency) -> CentroTreinamentoOut:
    centro_treinamento: CentroTreinamentoOut = (await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))
                              ).scalars().first()
    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
            , detail='Centro de treinamento não encontrado'
        )

    return centro_treinamento