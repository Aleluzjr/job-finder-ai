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
        nome=extracted_data.get("nome"),
        cargo=extracted_data.get("cargo"),
        habilidades=str(extracted_data.get("skills")),
        experiencias=str(extracted_data.get("experiencias")),
        certificacoes=str(extracted_data.get("certificacoes")),
        perfil_ia=ai_profile
    )
    db.add(candidato)
    db.commit()
    db.refresh(candidato)

    return {
        "id": candidato.id,
        "dados_extraidos": extracted_data,
        "perfil_gerado": ai_profile
    }