from pydantic import BaseModel


class Vacancy(BaseModel):
    uuid: str
    name: str
    keywords: str | None = ""
    description: str | None = ""
    comment: str | None = ""
    requested_experience: int | None = 0
