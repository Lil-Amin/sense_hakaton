from pydantic import BaseModel

from resume_filter.models.resume import Resume
from resume_filter.models.vacancy import Vacancy


class SortedCandidateSelection(BaseModel):
    vacancy: Vacancy
    confirmed_resumes: list[Resume]
    failed_resumes: list[Resume]
