# app/resume_reader.py
import os
import google.generativeai as genai
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import json

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
print(os.getenv("GOOGLE_API_KEY"))


def extract_json_from_text(text):
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        return match.group()
    return None

def analyze_resume(text):
    prompt = f"""
Você é um assistente de RH. Analise o seguinte currículo e retorne **somente um JSON válido** e puro, sem explicações antes ou depois.

Campos esperados:
- Nome completo
- Cidade/Estado
- Telefone de contato
- link do linkedin
- Cargo atual ou mais recente
- Lista de habilidades (skills)
- Experiências profissionais (cargo, empresa, período, atividades)
- Certificações (se houver)
- Idiomas (se houver)
- Palavras-chaves (Ex: ERP, CRM, TOTVS RM, Rubeus, Integração de sistemas, Mapeamento de processos,
                   Levantamento de requisitos, BPMN, SQL, Dashboards, Automatização de processos, Usuarios)

Currículo:
{text}
"""

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)

    raw_text = response.text
    json_str = extract_json_from_text(raw_text)

    if json_str:
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print("Erro ao decodificar JSON:", e)
            print("Tentativa de JSON:", json_str)
            return {}
    else:
        print("❌ JSON não encontrado na resposta do Gemini.")
        print("Resposta completa:", raw_text)
        return {}