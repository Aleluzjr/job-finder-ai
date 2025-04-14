from fastapi import FastAPI, UploadFile, File
from app.resume_reader import extract_text_from_pdf, analyze_resume, generate_ai_profile
from app.database import SessionLocal, Candidato
import json

# ✅ Defina o app aqui antes de usar qualquer @app
app = FastAPI()
@app.post("/upload/")
async def upload_resume(file: UploadFile = File(...)):
    contents = await file.read()
    with open("temp.pdf", "wb") as f:
        f.write(contents)

    with open("temp.pdf", "rb") as f:
        text = extract_text_from_pdf(f)

    extracted_data = analyze_resume(text)
    ai_profile = generate_ai_profile(text)

    db = SessionLocal()
    candidato = Candidato(
        NOME=extracted_data.get("Nome completo", ""),
        CIDADE=extracted_data.get("Cidade/Estado", "").split("/")[0] if extracted_data.get("Cidade/Estado") else "",
        ESTADO=extracted_data.get("Cidade/Estado", "").split("/")[1] if extracted_data.get("Cidade/Estado") and "/" in extracted_data.get("Cidade/Estado") else "",
        TELEFONE=extracted_data.get("Telefone de contato", ""),
        LINKEDIN=extracted_data.get("link do linkedin", ""),
        CARGO=extracted_data.get("Cargo atual ou mais recente", ""),
        HABILIDADES=str(extracted_data.get("Lista de habilidades (skills)", "")),
        EXPERIENCIAS=str(extracted_data.get("Experiências profissionais", "")),
        CERTIFICACOES=str(extracted_data.get("Certificações (se houver)", "")),
        IDIOMAS=str(extracted_data.get("Idiomas (se houver)", "")),
        PALAVRAS_CHAVES=str(extracted_data.get("Palavras-chaves", ""))
    )
    db.add(candidato)
    db.commit()
    db.refresh(candidato)
    return {"msg": "Currículo processado e salvo com sucesso!", "id": candidato.ID,
                "dados_extraidos": extracted_data,
                "perfil_gerado": ai_profile}
