from fastapi import APIRouter, Body, HTTPException, status, Depends, FastAPI
from fastapi_pagination import Page, Params, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate as paginate_sqlalchemy
from pydantic import UUID4
from uuid import uuid4
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from workout_api.contrib.dependencies import DataBaseDependency
from workout_api.categorias.schemas import CategoriaIn, CategoriaOut
from workout_api.categorias.models import CategoriaModel

router = APIRouter()
app = FastAPI()
add_pagination(app)
app.include_router(router)

@router.post(path='/',
             summary='Criar nova categoria'
             , status_code=status.HTTP_201_CREATED
             , response_model=CategoriaOut)
async def post(
           db_session: DataBaseDependency,
           categoria_in: CategoriaIn = Body(...)
    ) -> CategoriaOut:

    try:
        categoria_out = CategoriaOut(id=uuid4(), **categoria_in.model_dump())
        categoria_model = CategoriaModel(**categoria_out.model_dump())
        db_session.add(categoria_model)
        await db_session.commit()

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f'Já existe uma categoria com o nome: {categoria_in.nome}.'
        )
        db_session.rollback()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Ocorreu um erro ao inserir os dados no banco: {e}'
        )
        db_session.rollback()

    return categoria_out

@router.get(path='/',
             summary='Obter todas as categorias'
             , status_code=status.HTTP_200_OK
             , response_model=list[CategoriaOut])
async def query(db_session: DataBaseDependency) -> list[CategoriaOut]:
    categorias: list[CategoriaOut] = (await db_session.execute(select(CategoriaModel))
                                     ).scalars().all()
    return categorias

@router.get(path='/paginate',
             summary='Obter todas as categorias com paginação'
             , status_code=status.HTTP_200_OK
             , response_model=Page[CategoriaOut])
async def get_categorias(db_session: DataBaseDependency, params: Params = Depends()) -> Page[CategoriaOut]:
    categorias = select(CategoriaModel).order_by(CategoriaModel.nome)
    return await paginate_sqlalchemy(db_session, categorias, params)

@router.get(path='/{id}',
             summary='Obter categoria por Id'
             , status_code=status.HTTP_200_OK
             , response_model=CategoriaOut)
async def query(id: UUID4, db_session: DataBaseDependency) -> CategoriaOut:
    categoria: CategoriaOut = (await db_session.execute(select(CategoriaModel).filter_by(id=id))
                              ).scalars().first()
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
            , detail='Categoria não encontrada'
        )

    return categoria