# API E-Commerce: Gerenciamento de Produtos

API RESTful construída com FastAPI e SQLAlchemy para gerenciamento de catálogo de produtos, com suíte de testes robusta utilizando Pytest e bancos de dados isolados via Docker.

## Instruções para execução

### 1. Subindo a infraestrutura
Para subir o banco de dados de desenvolvimento e o de testes:
```bash
docker-compose up -d db_test
docker-compose up -d db_dev