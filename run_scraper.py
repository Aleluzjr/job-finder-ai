import asyncio
from app.scrapers.gupy_scraper import scrape_gupy_vagas, salvar_no_banco
import logging

def main():
    print("Iniciando execução do scraper da Gupy...")
    vagas = asyncio.run(scrape_gupy_vagas())
    
    if vagas:
        print(f"Total de vagas encontradas: {len(vagas)}")
        salvar_no_banco(vagas)
        print("Vagas salvas no banco de dados.")
    else:
        print("Nenhuma vaga foi encontrada.")
    
    print("\nVerifique o arquivo 'gupy_scraper.log' para mais detalhes sobre a execução.")

if __name__ == "__main__":
    main() 