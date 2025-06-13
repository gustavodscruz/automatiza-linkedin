from fastapi import FastAPI

from domain.linkedin import LinkedinController
from domain.linkedin.certificados import CertificadoController
from utils.database import Base, DatabaseManager
import uvicorn

instace = DatabaseManager.getInstance()
Base.metadata.create_all(bind=instace.engine)

app = FastAPI(
    title="API de extração do linkedin",
    description="Serve para extrair certificados do Linkedin",
    version="0.0.1",
    docs_url="/",
    openapi_tags=[
        {
            "name": "Certificados",
            "description" : "Operações com certificados"
        },
        {
            "name": "Linkedin",
            "description" : "Operações com Linkedin"
        }
    ]
)

app.include_router(LinkedinController.router)
app.include_router(CertificadoController.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)


