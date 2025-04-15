from database import SessionLocal
from models import JOB_OFFERS

def salvar_vaga(dados):
    session = SessionLocal()
    vaga = JOB_OFFERS(
        SITE=dados["site"],
        TITULO=dados["titulo"],
        EMPRESA=dados["empresa"],
        LOCALIDADE=dados["localidade"],
        MODALIDADE=dados["modalidade"],
        DESCRICAO=dados["descricao"],
        URL=dados["url"]
    )
    session.add(vaga)
    session.commit()
    session.close()
