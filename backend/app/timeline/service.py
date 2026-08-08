from app.services.medical_record_service import get_all_medical_records


def generate_timeline(user_id: str):

    records = get_all_medical_records(user_id)

    # Keep your existing timeline logic below this line

    # keep the rest of your existing timeline logic here

    timeline = []

    for record in records:

        event = {
            "date": record["dates"][0] if record.get("dates") else "Unknown",
            "title": (
                record["diagnosis"][0]
                if record.get("diagnosis")
                else "Medical Report"
            ),
            "doctor": record.get("doctor"),
            "hospital": record.get("hospital"),
            "diagnosis": record.get("diagnosis", [])
        }

        timeline.append(event)

    timeline.sort(key=lambda x: x["date"])

    return timeline
