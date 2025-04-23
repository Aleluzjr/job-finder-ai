import asyncio
from app.database import SessionLocal
from models import JOB_OFFERS
from app.scrapers.gupy_scraper import scrape_gupy_vagas
from datetime import datetime

def salvar_vagas(vagas: list):
    db = SessionLocal()
    try:
        for vaga in vagas:
            if not vaga.get("titulo") or not vaga.get("url"):
                continue  # ignora vagas incompletas

            # Verifica se a vaga já existe no banco (baseado na URL)
            existente = db.query(JOB_OFFERS).filter(JOB_OFFERS.url == vaga["url"]).first()
            if not existente:
                nova_vaga = JOB_OFFERS(**vaga)
                db.add(nova_vaga)
        
        db.commit()
    finally:
        db.close()


import logging
logging.basicConfig(level=logging.INFO)

def coletar_e_salvar_vagas():
    logging.info("Iniciando coleta de vagas...")
    vagas = asyncio.run(scrape_gupy_vagas())
    if vagas:
        salvar_vagas(vagas)
        logging.info(f"{len(vagas)} vagas salvas.")
        return {"status": "ok", "total": len(vagas)}
    logging.warning("Nenhuma vaga encontrada.")
    return {"status": "sem resultados", "total": 0}



def listar_vagas():
    db = SessionLocal()
    try:
        return db.query(JOB_OFFERS).order_by(JOB_OFFERS.data_coleta.desc()).limit(50).all()
    finally:
        db.close()

