from pydantic import BaseModel

from resume_filter.models.vacancy import Vacancy
from resume_filter.models.resume import Resume


class SortedCandidateSelection(BaseModel):
    vacancy: Vacancy
    confirmed_resumes: list[Resume]
    failed_resumes: list[Resume]
