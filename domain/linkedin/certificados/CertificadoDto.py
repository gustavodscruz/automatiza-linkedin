from pydantic import BaseModel

class CertificadoDto(BaseModel):
    titulo: str
    empresa: str
    data_validacao: str
    link_url: str


class CertificadoDtoResponse(BaseModel):
    id: int
    titulo: str
    empresa: str
    data_validacao: str
    link_url: str


