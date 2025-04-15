from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func
from app.database import Base

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

class JOB_OFFERS(Base):
    __tablename__ = "JOB_OFFERS"

    ID = Column(Integer, primary_key=True, autoincrement=True)
    SITE = Column(String(50))
    TITULO = Column(String(255))
    EMPRESA = Column(String(255))
    LOCALIDADE = Column(String(100))
    MODALIDADE = Column(String(50))
    DESCRICAO = Column(Text)
    URL = Column(Text)
    DATA_COLETA = Column(TIMESTAMP, default=func.now())