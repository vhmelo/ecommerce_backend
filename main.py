import logging
import time
from fastapi import FastAPI, Request
from routers import produtos

# ================= Configuração de Logs =================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("ecommerce_api")

# ================= API e Rotas =================
app = FastAPI(
    title="E-commerce API",
    description="API arquitetada em camadas com FastAPI, SQLAlchemy, Alembic (Migrações), validação Pydantic e Logs.",
    version="2.0.0"
)

# Acopla as rotas modulares na aplicação principal
app.include_router(produtos.router)

# ================= Middleware de Logs =================
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Processa a requisição e envia para o router
    response = await call_next(request)
    
    # Calcula o tempo total
    process_time = time.time() - start_time
    
    # Imprime no terminal o registro da operação
    logger.info(
        f"Acesso: {request.method} {request.url.path} "
        f"| Status: {response.status_code} "
        f"| Tempo: {process_time:.4f}s"
    )
    return response