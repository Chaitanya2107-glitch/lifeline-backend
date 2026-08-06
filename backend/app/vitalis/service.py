from app.services.medical_record_service import get_all_medical_records
from app.summary.service import generate_summary
from app.ai.providers.groq_provider import generate


def generate_vitalis_response(
    user_id: int,
    question: str,
):

    records = get_all_medical_records(user_id)

    if not records:
        return "No medical records found."

    summary = generate_summary(user_id)

    context = f"""
Patient Medical Summary:

{summary}


Medical Records:

"""

    for record in records:
        context += f"""
Date:
{record.get("created_at")}

Doctor:
{record.get("doctor")}

Hospital:
{record.get("hospital")}

Diagnosis:
{record.get("diagnosis")}

Medicines:
{record.get("medicines")}

---

"""

    prompt = f"""
You are Vitalis, a medical assistant.

Use only the provided patient information.

Do not create medical facts that are not present.

Do not answer using external knowledge about the patient's history.

If the answer is unavailable, clearly say:
"I don't have enough information in your medical records."

Patient Information:

{context}

Question:

{question}

Answer:
"""

    return generate(prompt)
