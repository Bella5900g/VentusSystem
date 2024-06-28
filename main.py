from fastapi import FastAPI
from routers import client, service, technician

app = FastAPI()

app.include_router(client.router, prefix="/api/v1")
app.include_router(service.router, prefix="/api/v1")
app.include_router(technician.router, prefix="/api/v1")

# Executar o servidor: uvicorn main:app --reload
