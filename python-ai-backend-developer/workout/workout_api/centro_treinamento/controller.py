from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from uuid import uuid4
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from workout_api.contrib.dependencies import DataBaseDependency
from workout_api.centro_treinamento.schemas import CentroTreinamentoIn, CentroTreinamentoOut
from workout_api.centro_treinamento.models import CentroTreinamentoModel

router = APIRouter()

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

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ocorreu um erro ao inserir os dados no banco'
        )

    return centro_treinamento_out


@router.get(path='/',
             summary='Obter todos os centros de treinamento'
             , status_code=status.HTTP_200_OK
             , response_model=list[CentroTreinamentoOut])
async def query(db_session: DataBaseDependency) -> list[CentroTreinamentoOut]:
    centros_treinamento: list[CentroTreinamentoOut] = (await db_session.execute(select(CentroTreinamentoModel))
                                      ).scalars().all()
    return centros_treinamento

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