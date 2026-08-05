from app.database.supabase import supabase


def get_record_by_hash(report_hash: str):
    response = (
        supabase
        .table("medical_records")
        .select("*")
        .eq("report_hash", report_hash)
        .limit(1)
        .execute()
    )

    if response.data:
        return response.data[0]

    return None



def save_medical_record(record: dict):
    response = (
        supabase
        .table("medical_records")
        .insert(record)
        .execute()
    )

    return response.data[0]
