from fastapi import FastAPI
from routers import client, service, technician, stock, appointment, financial, report

app = FastAPI()

app.include_router(client.router, prefix="/api/v1")
app.include_router(service.router, prefix="/api/v1")
app.include_router(technician.router, prefix="/api/v1")
app.include_router(stock.router, prefix="/api/v1")
app.include_router(appointment.router, prefix="/api/v1")
app.include_router(financial.router, prefix="/api/v1")
app.include_router(report.router, prefix="/api/v1")

# Executar o servidor: uvicorn main:app --reload
