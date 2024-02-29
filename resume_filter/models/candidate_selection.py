from pydantic import BaseModel

from resume_filter.models.vacancy import Vacancy
from resume_filter.models.resume import Resume


class CandidateSelection(BaseModel):
    vacancy: Vacancy
    resumes: list[Resume]
