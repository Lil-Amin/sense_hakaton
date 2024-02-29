from pydantic import BaseModel


class Vacancy(BaseModel):
    uuid: str
    name: str
    keywords: str
    description: str
    comment: str
    requested_experience: int
    # failed_resumes: list[Resume]
    # confirmed_resumes: list[Resume]
