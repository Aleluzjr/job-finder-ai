from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://usuario:senha@localhost:5432/job_finder")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class Candidato(Base):
    __tablename__ = "candidatos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    cargo = Column(String)
    habilidades = Column(Text)
    experiencias = Column(Text)
    certificacoes = Column(Text)
    perfil_ia = Column(Text)

def init_db():
    Base.metadata.create_all(bind=engine)
