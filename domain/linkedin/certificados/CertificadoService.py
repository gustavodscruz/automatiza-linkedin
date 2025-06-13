from sqlalchemy.orm import Session

from domain.linkedin.certificados.CertificadoDto import CertificadoDto, CertificadoDtoResponse
from domain.linkedin.certificados.CertificadoModel import Certificado

class CertificadoService:
    def __init__(self, db: Session):
        self.db = db

    def save(self, certificado_dto: CertificadoDto):
        try:
            db_certificado = Certificado(**certificado_dto.model_dump())
            self.db.add(db_certificado)
            self.db.commit()
            self.db.refresh(db_certificado)
            return db_certificado
        except Exception as e:
            self.db.rollback()
            raise e

    def save_all(self, certificados: list[CertificadoDto]):
        try:
            db_certificados = [Certificado(**certificado.model_dump()) for certificado in certificados]
            self.db.add_all(db_certificados)
            self.db.commit()
            return db_certificados
        except Exception as e:
            self.db.rollback()
            raise e

    def list_all(self):
        return self.db.query(CertificadoDto).all()

    def get_by_id(self, id: int):
        return self.db.query(Certificado).filter(Certificado.id == id).first()

    def delete(self, id: int):
        return self.db.query(Certificado).filter(Certificado.id == id).delete()

    def update(self, id: int, certificado: CertificadoDto):
        return self.db.query(Certificado).filter(Certificado.id == id).update(
            {key: value for key, value in certificado.model_dump().items() if value is not None}
        )
