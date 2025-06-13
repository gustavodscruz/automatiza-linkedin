from sqlalchemy import Column, String, Integer

from utils.database import Base

class Certificado(Base):
    __tablename__ = 'certificado'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    titulo = Column(String(200), nullable=False)
    empresa = Column(String(200), nullable=False)
    data_validacao = Column(String(200), nullable=False)
    link_url = Column(String(200), nullable=False)