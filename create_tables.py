from app.database import Base, engine  # Ajuste o caminho conforme seu projeto
from app.models import Candidato       # Importa o modelo para que ele seja registrado no Base

def create_all_tables():
    print("📦 Criando tabelas no banco de dados...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas com sucesso!")

if __name__ == "__main__":
    create_all_tables()
