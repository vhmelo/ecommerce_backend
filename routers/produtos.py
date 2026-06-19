import logging
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from database import get_db
from models import ProdutoDB
from schemas import ProdutoCreate, ProdutoResponse

# Puxa o logger configurado no main.py
logger = logging.getLogger("ecommerce_api")

router = APIRouter(prefix="/produtos", tags=["Produtos"])

@router.post("", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED, summary="Cria um novo produto")
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    db_produto = ProdutoDB(**produto.model_dump())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    
    logger.info(f"Produto adicionado ao catálogo: '{db_produto.nome}' (ID: {db_produto.id})")
    return db_produto

@router.get("", response_model=list[ProdutoResponse], summary="Lista produtos com paginação")
def listar_produtos(
    skip: int = Query(0, description="Número de registros para pular", ge=0),
    limit: int = Query(100, description="Limite máximo", le=100),
    db: Session = Depends(get_db)
):
    return db.query(ProdutoDB).offset(skip).limit(limit).all()

@router.get("/{id}", response_model=ProdutoResponse, summary="Busca um produto específico")
def buscar_produto(id: int, db: Session = Depends(get_db)):
    produto = db.query(ProdutoDB).filter(ProdutoDB.id == id).first()
    if not produto:
        logger.warning(f"Busca falhou: Produto ID {id} inexistente.")
        raise HTTPException(status_code=404, detail="Produto não encontrado no catálogo")
    return produto

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Remove um produto")
def deletar_produto(id: int, db: Session = Depends(get_db)):
    produto = db.query(ProdutoDB).filter(ProdutoDB.id == id).first()
    if not produto:
        logger.warning(f"Deleção falhou: Produto ID {id} inexistente.")
        raise HTTPException(status_code=404, detail="Produto não encontrado no catálogo")
    db.delete(produto)
    db.commit()
    
    logger.info(f"Produto deletado com sucesso: ID {id}")
    return None