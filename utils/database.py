from contextlib import contextmanager
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
import logging
import os

logger = logging.getLogger(__name__)
Base = declarative_base()

class DatabaseManager:
    __instance = None

    def __init__(self):
        if DatabaseManager.__instance is not None:
            raise Exception("This class is a singleton!")

        DATABASE_URL = os.getenv(
            "DATABASE_URL",
            "mysql+mysqlconnector://root:senha@localhost:3306/teste"
        )

        try:
            self.engine = create_engine(
                DATABASE_URL,
                pool_pre_ping=True,  # Verifica conexões antes de usar
                pool_size=5,         # Tamanho do pool de conexões
                max_overflow=10      # Conexões extras permitidas
            )
            self.SessionLocal = sessionmaker(
                autoflush=False,
                autocommit=False,
                bind=self.engine
            )
            logger.info("Conexão com banco de dados estabelecida com sucesso")
        except Exception as e:
            logger.error(f"Erro ao conectar ao banco de dados: {e}")
            raise

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    @contextmanager
    def get_db(self) -> Generator[Session, None, None]:
        session = self.SessionLocal()
        try:
            logger.debug("Iniciando nova sessão do banco de dados")
            yield session
            # Commit automático se não houver exceções
            session.commit()
            logger.debug("Sessão commitada com sucesso")
        except SQLAlchemyError as e:
            logger.error(f"Erro na sessão do banco de dados: {e}")
            session.rollback()
            raise
        finally:
            logger.debug("Fechando sessão do banco de dados")
            session.close()

# Dependency para o FastAPI
def get_db():
    db_manager = DatabaseManager.getInstance()
    with db_manager.get_db() as session:
        yield session