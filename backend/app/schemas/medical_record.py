from pydantic import BaseModel, Field


class MedicalRecord(BaseModel):
    diagnosis: list[str] = Field(default_factory=list)
    medicines: list[str] = Field(default_factory=list)
    allergies: list[str] = Field(default_factory=list)

    doctor: str | None = None
    hospital: str | None = None

    dates: list[str] = Field(default_factory=list)

    lab_values: dict[str, str] = Field(default_factory=dict)

    raw_text: str
