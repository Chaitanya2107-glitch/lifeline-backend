from app.database.supabase import supabase


def save_medical_record(record: dict):
    response = (
        supabase
        .table("medical_records")
        .insert(record)
        .execute()
    )

    return response.data[0]
