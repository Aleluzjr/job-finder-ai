from playwright.sync_api import sync_playwright
import time
from database import SessionLocal
from models import JOB_OFFERS


def scrape_gupy_jobs(cargo="Analista", localidade="", modelo_trabalho=""):
    results = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        url = f"https://portal.gupy.io/job-search?jobBoard=internet&keyword={cargo}"
        page.goto(url)
        time.sleep(5)  # Aguarda o carregamento

        # Scroll para carregar mais vagas (pode ajustar o número de scrolls)
        for _ in range(3):
            page.mouse.wheel(0, 5000)
            time.sleep(2)

        job_cards = page.query_selector_all("[data-testid='job-list__item']")

        for card in job_cards:
            titulo = card.query_selector("h2")
            empresa = card.query_selector("[data-testid='job-list__company']")
            local = card.query_selector("[data-testid='job-list__location']")
            link = card.query_selector("a")

            titulo = titulo.inner_text().strip() if titulo else ""
            empresa = empresa.inner_text().strip() if empresa else ""
            local = local.inner_text().strip() if local else ""
            url = link.get_attribute("href") if link else ""

            # Filtros opcionais
            if localidade and localidade.lower() not in local.lower():
                continue
            if modelo_trabalho and modelo_trabalho.lower() not in local.lower():
                continue

            results.append({
                "titulo": titulo,
                "empresa": empresa,
                "localidade": local,
                "modalidade": modelo_trabalho,
                "url": url,
                "site": "Gupy"
            })

        browser.close()
    return results


if __name__ == "__main__":
    vagas = scrape_gupy_jobs(cargo="Analista de Sistemas", localidade="Remoto")
    for vaga in vagas:
        print(vaga)  # Ou salve no banco de dados

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
