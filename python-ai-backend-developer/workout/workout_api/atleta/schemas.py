from pydantic import Field, PositiveFloat
from typing import Annotated
from workout_api.categorias.schemas import CategoriaIn
from workout_api.centro_treinamento.schemas import CentroTreinamentoAtleta
from workout_api.contrib.schemas import BaseSchema, OutMixin

class Atleta(BaseSchema):
    nome: Annotated[str, Field(description="Nome do atleta", max_length=50)]
    cpf: Annotated[str, Field(description="CPF do atleta", max_length=11)]
    idade: Annotated[int, Field(description="Idade do atleta")]
    peso: Annotated[PositiveFloat, Field(description="Peso do atleta")]
    altura: Annotated[PositiveFloat, Field(description="Altura do atleta")]
    sexo: Annotated[str, Field(description="Sexo do atleta", examples="M", max_length=1)]
    categoria: Annotated[CategoriaIn, Field(description='Categoria do atleta')]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description='Centro de treinamento do atleta')]

class AtletaIn(Atleta):
    pass
class AtletaOut(Atleta, OutMixin):
    pass

