from .index import client, model








def generate_summary(data) -> str:


	prompt = f"""
		You are an expert resume writer and career coach.

		TASK:
		Generate a concise, professional resume summary based on the user's experience and skills.

		RULES (STRICT):
		- Return ONLY plain text
		- No markdown
		- No bullet points
		- No headings
		- No explanations
		- 2–4 sentences maximum
		- Professional, confident, ATS-friendly tone
		- Do NOT mention "AI", "assistant", or "generated"

		CONTENT GUIDELINES:
		- Highlight role, experience level, and key strengths
		- Emphasize impact, responsibilities, and skills
		- If experience is limited, focus on skills and potential
		- If data is missing, generate realistic professional content

		USER DATA (JSON):
		{{
		  "experiences": {data["experiences"]},
		  "skills": {data["skills"]}
		}}

		OUTPUT:
		Return ONLY the resume summary text.
	"""


	response = client.chat.completions.create(
		model=model,
		messages=[{"role": "user", "content": prompt}],
        temperature=0.25,
	)

	summary_text = response.choices[0].message.content.strip()

	return summary_text
