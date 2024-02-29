from pydantic import BaseModel

from resume_filter.models.experience_item import ExperienceItem
from resume_filter.models.education_item import EducationItem


class Resume(BaseModel):
    uuid: str
    first_name: str
    last_name: str
    birth_date: str
    country: str
    city: str
    about: str
    key_skills: str
    experienceItem: list[ExperienceItem]
    educationItem: list[EducationItem]
    languageItems: list[str]

