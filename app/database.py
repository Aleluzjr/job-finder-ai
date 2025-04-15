from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://usuario:senha@localhost:5432/job_finder")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class Candidato(Base):
    __tablename__ = "CANDIDATOS"

    ID = Column(Integer, primary_key=True, index=True)
    NOME = Column(String)
    CIDADE = Column(String)
    ESTADO = Column(String)
    TELEFONE = Column(String)
    LINKEDIN = Column(String)
    CARGO = Column(String)
    HABILIDADES = Column(Text)
    EXPERIENCIAS = Column(Text)
    CERTIFICACOES = Column(Text)
    IDIOMAS = Column(Text)
    PALAVRAS_CHAVES = Column(Text)

def init_db():
    Base.metadata.create_all(bind=engine)
