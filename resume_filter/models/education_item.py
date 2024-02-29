from pydantic import BaseModel


class EducationItem(BaseModel):
    year: str
    organization: str
    faculty: str
    specialty: str
    result: str
    education_type: str
    education_level: str
