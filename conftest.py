import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import Base, get_db
from models import ProdutoDB

TEST_DATABASE_URL = "postgresql://test_user:test_password@127.0.0.1:5433/test_db"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def client():
    Base.metadata.create_all(bind=engine)
    
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
            
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as c:
        yield c
        
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()

@pytest.fixture()
def produto_existente(client):
    db = TestingSessionLocal()
    produto = ProdutoDB(nome="Produto Fixture", preco=50.0, estoque=10, ativo=True)
    db.add(produto)
    db.commit()
    db.refresh(produto)
    db.close()
    return produto