from pydantic import BaseModel


class EducationItem(BaseModel):
    year: int | None
    organization: str
    faculty: str
    specialty: str | None
    result: str | None
    education_type: str
    education_level: str | None
