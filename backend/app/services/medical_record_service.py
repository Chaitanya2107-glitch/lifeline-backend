from app.database.supabase import supabase


def get_record_by_hash(user_id: str, report_hash: str):
    response = (
        supabase
        .table("medical_records")
        .select("*")
        .eq("user_id", user_id)
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
def get_all_medical_records(user_id: str):
    response = (
        supabase
        .table("medical_records")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )

    return response.data
