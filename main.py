from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import client, service, technician, stock, appointment, financial, report

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas as origens, para desenvolvimento local
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos os cabeçalhos
)

app.include_router(client.router, prefix="/api/v1")
app.include_router(service.router, prefix="/api/v1")
app.include_router(technician.router, prefix="/api/v1")
app.include_router(stock.router, prefix="/api/v1")
app.include_router(appointment.router, prefix="/api/v1")
app.include_router(financial.router, prefix="/api/v1")
app.include_router(report.router, prefix="/api/v1")

# Executar o servidor: uvicorn main:app --reload
