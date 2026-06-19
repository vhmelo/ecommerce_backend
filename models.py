from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base

class ProdutoDB(Base):
    __tablename__ = "produtos"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    estoque = Column(Integer, default=0)
    ativo = Column(Boolean, default=True)