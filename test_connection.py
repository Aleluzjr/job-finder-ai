from app.database import engine

try:
    with engine.connect() as conn:
        print("✅ Conexão com banco de dados bem-sucedida!")
except Exception as e:
    print("❌ Erro ao conectar:", e)
