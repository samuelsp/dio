# Workout API

## Descrição

Esta é uma API desenvolvida em Python para gerenciar atletas, categorias e centros de treinamento. A API permite criar, ler, atualizar e deletar informações sobre atletas, categorias e centros de treinamento.

## Endpoints

### Atleta Controller

- `POST /`: Cria um novo atleta.
- `GET /`: Obtém todos os atletas.
- `GET /paginate`: Obtém todos os atletas com paginação.
- `GET /resumo`: Obtém todos os atletas com response personalizado.
- `GET /{id}`: Obtém atleta por Id.
- `PATCH /{id}`: Edita um atleta pelo id.
- `DELETE /{id}`: Deleta um atleta pelo id.

### Categoria Controller

- `GET /paginate`: Obtém todas as categorias com paginação.
- `GET /{id}`: Obtém categoria por Id.

### Centro de Treinamento Controller

- `POST /`: Cria um novo centro de treinamento.
- `GET /`: Obtém todos os centros de treinamento.
- `GET /paginate`: Obtém todos os centros de treinamento com paginação.
- `GET /{id}`: Obtém centro de treinamento por Id.

## Como clonar e executar o projeto

1. Clone o repositório: `git clone https://github.com/samuelsp/dio/tree/main/python-ai-backend-developer/workout`
2. Navegue até a pasta do projeto: `cd <workout>`
3. Instale as dependências: `pip install -r requirements.txt`
4. Execute o projeto: `make run`

## Principais pacotes de software utilizados

- FastAPI
- SQLAlchemy
- FastAPI Pagination
- Pydantic