# API E-commerce: Gerenciamento de Produtos

Esta é uma API RESTful desenvolvida em Python para o gerenciamento de um catálogo de produtos de um e-commerce. O projeto foi construído seguindo boas práticas de engenharia de software, utilizando uma arquitetura modularizada e versionamento de banco de dados.

**Tecnologias utilizadas:**
* FastAPI (Framework web de alta performance)
* SQLAlchemy (ORM para modelagem de dados)
* Alembic (Versionamento e migrações do banco de dados)
* Pydantic V2 (Validação estrita de dados e schemas)
* PostgreSQL (Banco de dados relacional orquestrado via Docker)
* Pytest (Suíte de testes automatizados com cobertura)

---

## 1. Instruções para subir o banco de teste com Docker

A infraestrutura da aplicação conta com dois bancos de dados PostgreSQL isolados: um para desenvolvimento e outro exclusivo para testes automatizados. Ambos são gerenciados via Docker Compose.

Para subir a infraestrutura, certifique-se de ter o Docker instalado e rodando na sua máquina. Em seguida, abra o terminal na raiz do projeto e execute o comando abaixo para iniciar os containers em segundo plano:
docker-compose up -d

Verificação de status:
Para garantir que os bancos estão prontos para receber conexões, execute docker ps e verifique se o status dos containers db_dev (porta 5435) e db_test (porta 5433) consta como (healthy).

## 2. Comando exato para executar os testes
Antes de executar os testes, certifique-se de que o seu ambiente virtual Python está ativado e as dependências do requirements.txt estão instaladas.

Para executar a suíte completa de testes com detalhamento de cada função e gerar o relatório de cobertura de código (coverage), utilize o comando exato abaixo:

Bash
pytest --cov=main --cov=routers -v

## 3. Saída esperada do Pytest
Ao executar o comando acima com o container db_test rodando de forma saudável, a saída no terminal deverá ser idêntica à apresentada abaixo, registrando sucesso (PASSED) em todos os 15 testes de integração e validação, além de 100% de cobertura.

Plaintext
============================= test session starts ==============================
platform win32 -- Python 3.13.14, pytest-9.1.0, pluggy-1.6.0
rootdir: C:\Users\UNIVASSOURAS\Documents\gerenciamento_produtos
plugins: anyio-4.14.0, cov-7.1.0
collected 15 items

tests/test_produtos.py::test_listar_produtos_banco_vazio PASSED           [  6%]
tests/test_produtos.py::test_criar_produto_persistencia PASSED            [ 13%]
tests/test_produtos.py::test_criar_produto_aparece_na_listagem PASSED     [ 20%]
tests/test_produtos.py::test_buscar_produto_por_id_sucesso PASSED         [ 26%]
tests/test_produtos.py::test_buscar_produto_inexistente PASSED            [ 33%]
tests/test_produtos.py::test_deletar_produto PASSED                       [ 40%]
tests/test_produtos.py::test_deletar_produto_confirma_remocao PASSED      [ 46%]
tests/test_produtos.py::test_deletar_produto_inexistente PASSED           [ 53%]
tests/test_produtos.py::test_criar_produto_payload_invalido[payload0] PASSED [ 60%]
tests/test_produtos.py::test_criar_produto_payload_invalido[payload1] PASSED [ 66%]
tests/test_produtos.py::test_criar_produto_payload_invalido[payload2] PASSED [ 73%]
tests/test_produtos.py::test_criar_produto_payload_invalido[payload3] PASSED [ 80%]
tests/test_produtos.py::test_criar_produto_payload_invalido[payload4] PASSED [ 86%]
tests/test_produtos.py::test_isolamento_1_adiciona_produto PASSED         [ 93%]
tests/test_produtos.py::test_isolamento_2_banco_deve_estar_limpo PASSED   [100%]

---------- coverage: platform win32, python 3.13.14-final-0 ----------
Name                 Stmts   Miss  Cover
----------------------------------------
main.py                 20      0   100%
routers/produtos.py     34      0   100%
----------------------------------------
TOTAL                   54      0   100%

============================== 15 passed in 0.85s ==============================

## 4. Isolamento entre Testes
A integridade da nossa suíte de testes é garantida por um estrito isolamento de estado, assegurando que o lixo residual de um teste não afete o resultado do próximo. Este mecanismo foi implementado no arquivo conftest.py através das seguintes estratégias:

Separação de Banco: Os testes nunca tocam no banco de dados de desenvolvimento. Utilizamos uma porta e um container exclusivos (db_test na porta 5433).

Dependency Injection: Utilizamos o recurso app.dependency_overrides do FastAPI para interceptar a injeção de dependência original (get_db) e forçar a API a utilizar a TestingSessionLocal.

Fixture com Ciclo de Vida (Yield): A fixture client atua como o controlador de estado:

Setup: Antes de cada teste iniciar, o comando Base.metadata.create_all é executado, gerando as tabelas limpas e vazias.

Yield: O TestClient é entregue para a função de teste realizar suas operações e validações.

Teardown: Assim que a função de teste finaliza (independente de sucesso ou falha), o fluxo retorna para a fixture e o comando Base.metadata.drop_all destrói todas as tabelas e dados gerados, deixando o PostgreSQL completamente zerado para o próximo ciclo.
