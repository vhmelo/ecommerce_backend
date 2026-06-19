import pytest

def test_listar_produtos_banco_vazio(client):
    response = client.get("/produtos")
    assert response.status_code == 200
    assert response.json() == []

def test_criar_produto_persistencia(client):
    payload = {"nome": "Teclado Mecânico", "preco": 250.0, "estoque": 15}
    response = client.post("/produtos", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["nome"] == "Teclado Mecânico"

def test_criar_produto_aparece_na_listagem(client):
    client.post("/produtos", json={"nome": "Monitor", "preco": 800.0})
    response = client.get("/produtos")
    assert len(response.json()) == 1
    assert response.json()[0]["nome"] == "Monitor"

def test_buscar_produto_por_id_sucesso(client, produto_existente):
    response = client.get(f"/produtos/{produto_existente.id}")
    assert response.status_code == 200
    assert response.json()["nome"] == "Produto Fixture"

def test_buscar_produto_inexistente(client):
    response = client.get("/produtos/9999")
    assert response.status_code == 404

def test_deletar_produto(client, produto_existente):
    response = client.delete(f"/produtos/{produto_existente.id}")
    assert response.status_code == 204

def test_deletar_produto_confirma_remocao(client, produto_existente):
    client.delete(f"/produtos/{produto_existente.id}")
    response = client.get(f"/produtos/{produto_existente.id}")
    assert response.status_code == 404

def test_deletar_produto_inexistente(client):
    response = client.delete("/produtos/9999")
    assert response.status_code == 404

# =========================================================================
# TESTE ROBUSTO DE VALIDAÇÃO (Abrangendo as novas regras do Pydantic)
# =========================================================================
@pytest.mark.parametrize("payload", [
    {"nome": "", "preco": 100.0},                  # Nome vazio
    {"nome": "   ", "preco": 100.0},               # Nome apenas com espaços 
    {"nome": "Mouse", "preco": 0},                 # Preço igual a zero
    {"nome": "Mouse", "preco": -15.5},             # Preço negativo
    {"nome": "Mouse", "preco": 50, "estoque": -5}, # Estoque negativo
    {"preco": 100.0},                              # Faltando nome
    {"nome": "Cabo USB"}                           # Faltando preço
])
def test_criar_produto_payload_invalido(client, payload):
    response = client.post("/produtos", json=payload)
    assert response.status_code == 422

def test_isolamento_1_adiciona_produto(client):
    client.post("/produtos", json={"nome": "Isolamento", "preco": 10.0})
    response = client.get("/produtos")
    assert len(response.json()) == 1

def test_isolamento_2_banco_deve_estar_limpo(client):
    response = client.get("/produtos")
    assert len(response.json()) == 0