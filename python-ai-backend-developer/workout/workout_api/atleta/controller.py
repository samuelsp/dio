from fastapi import APIRouter, Body, HTTPException, status
from workout_api.contrib.dependencies import DataBaseDependency
from workout_api.atleta.schemas import AtletaIn, AtletaOut

router = APIRouter()

@router.post(path='/'
             , summary='Criar novo atleta'
             , status_code=status.HTTP_201_CREATED
             #, response_model=AtletaOut
             )
async def post(
           #db_session: DataBaseDependency,
           #atleta_in: AtletaIn = Body(...)
    ):
    pass

