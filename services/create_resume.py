import os
import time
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from weasyprint import HTML

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[1]


BASE_TEMPLATES = BASE_DIR /"app" / "templates"
USER_TEMPLATES = BASE_DIR / "app" / "templates" / "user"



def generate_resume(
    *,
    user_id: int,
    job_description: str,
    user_data: dict,
    template_path: str,
) -> str:
    print("BASEDIR++======", BASE_DIR)
    print("BASE_TEMPLATES===========", BASE_TEMPLATES)

    with open(str(BASE_TEMPLATES / template_path / "index.html"), "r") as f:
        template_html = f.read()

    # 2️⃣ Groq client
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    # 3️⃣ AI PROMPT (STRICT)
    prompt = f"""
You are an AI resume editor.

STRICT RULES (MANDATORY):
- DO NOT change HTML structure
- DO NOT add or remove tags
- DO NOT modify classes, styles, or layout
- ONLY replace text inside existing tags

CONTENT RULES:
- Insert user data where it best fits
- If data is missing, generate realistic professional content
- Rewrite user text for grammar and clarity
- If no exact field exists, reuse closest section
- Keep tone professional and ATS-friendly

HTML TEMPLATE:
{template_html}

USER DATA (JSON):
{user_data}

JOB DESCRIPTION:
{job_description}

OUTPUT:
Return ONLY the final valid HTML string.
No markdown.
No explanations.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.25,
    )

    final_html = response.choices[0].message.content.strip()

    # 4️⃣ Create user output folder
    user_output_dir = USER_TEMPLATES / str(user_id)
    user_output_dir.mkdir(parents=True, exist_ok=True)

    pdf_dir = user_output_dir / str(int(time.time()))

    pdf_dir.mkdir(parents=True, exist_ok=True)

    # 5️⃣ Save PDF
    pdf_name = f"resume_{int(time.time())}.pdf"
    pdf_path = pdf_dir / pdf_name
    relative_pdf_path = os.path.relpath(pdf_path, start=BASE_TEMPLATES)

    HTML(
        string=final_html,
        base_url=str(BASE_TEMPLATES / template_path)
    ).write_pdf(pdf_path)

    return (
        relative_pdf_path,
        str(pdf_dir)
        )
