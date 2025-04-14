from sqlalchemy import Column, Integer, String, Text
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
