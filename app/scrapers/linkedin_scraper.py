import asyncio
from playwright.async_api import async_playwright
from datetime import datetime
from app.database import SessionLocal
from app.models import JOB_OFFERS


async def scrape_linkedin_vagas():
    vagas = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Personalize a URL de busca de vagas com base no filtro desejado
        search_url = (
            "https://www.linkedin.com/jobs/search/?keywords=Desenvolvedor%20Python"
            "&location=Brasil&f_WT=2&f_TP=1&f_E=2&f_JT=F"
        )

        await page.goto(search_url)
        await page.wait_for_timeout(5000)  # Espera o carregamento das vagas

        job_cards = await page.query_selector_all(".jobs-search-results__list-item")

        for card in job_cards:
            try:
                titulo = await card.query_selector_eval(".base-search-card__title", "e => e.innerText")
                empresa = await card.query_selector_eval(".base-search-card__subtitle", "e => e.innerText")
                localidade = await card.query_selector_eval(".job-search-card__location", "e => e.innerText")
                url = await card.query_selector_eval("a.base-card__full-link", "e => e.href")

                vaga = {
                    "site": "LinkedIn",
                    "titulo": titulo.strip(),
                    "empresa": empresa.strip(),
                    "localidade": localidade.strip(),
                    "modalidade": "Remoto ou Presencial",
                    "descricao": "",  # Pode ser completado depois se necessário
                    "url": url.strip(),
                    "data_coleta": datetime.now()
                }
                vagas.append(vaga)
            except Exception as e:
                print("Erro ao extrair vaga:", e)

        await browser.close()
    return vagas


def salvar_vagas_txt(vagas):
    with open("linkedin_vagas.txt", "w", encoding="utf-8") as f:
        for vaga in vagas:
            f.write(f"{vaga['titulo']} | {vaga['empresa']} | {vaga['localidade']} | {vaga['url']}\n")


def salvar_vagas_db(vagas):
    db = SessionLocal()
    try:
        for vaga in vagas:
            if not vaga.get("titulo") or not vaga.get("url"):
                continue
            existente = db.query(JOB_OFFERS).filter(JOB_OFFERS.url == vaga["url"]).first()
            if not existente:
                nova_vaga = JOB_OFFERS(**vaga)
                db.add(nova_vaga)
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    vagas_encontradas = asyncio.run(scrape_linkedin_vagas())
    if vagas_encontradas:
        salvar_vagas_txt(vagas_encontradas)
        salvar_vagas_db(vagas_encontradas)
        print(f"{len(vagas_encontradas)} vagas salvas.")
    else:
        print("Nenhuma vaga encontrada.")
