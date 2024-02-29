import datetime

from pydantic import BaseModel


class ExperienceItem(BaseModel):
    starts: datetime.datetime
    ends: datetime.datetime
    employer: str
    city: str
    position: str
    description: str

    # def __init__(self, starts, ends, employer, city, position, description):
    #     self.starts = datetime.strptime(starts, '%Y-%m-%d')
    #     self.ends = datetime.strptime(ends, '%Y-%m-%d') if ends else datetime.now()
    #     self.employer = employer
    #     self.city = city
    #     self.position = position
    #     self.description = description
