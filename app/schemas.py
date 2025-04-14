from pydantic import BaseModel

class CandidatoSchema(BaseModel):
    NOME: str
    CIDADE: str
    ESTADO: str
    TELEFONE: str
    LINKEDIN: str
    CARGO: str
    HABILIDADES: str
    EXPERIENCIAS: str
    CERTIFICACOES: str
    IDIOMAS: str
    PALAVRAS_CHAVES: str

    class Config:
        orm_mode = True
