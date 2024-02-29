from pydantic import BaseModel

from resume_filter.models.education_item import EducationItem
from resume_filter.models.experience_item import ExperienceItem


# TODO: maybe redo all str to str | None
class Resume(BaseModel):
    uuid: str
    first_name: str
    last_name: str
    birth_date: str | None
    country: str
    city: str
    about: str | None
    key_skills: str | None
    experienceItem: list[ExperienceItem] | None = None
    educationItem: list[EducationItem] | None = None
    languageItems: list[str] | None = None
