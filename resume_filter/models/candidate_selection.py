from pydantic import BaseModel

from resume_filter.models.resume import Resume
from resume_filter.models.vacancy import Vacancy


class CandidateSelection(BaseModel):
    vacancy: Vacancy
    resumes: list[Resume]
