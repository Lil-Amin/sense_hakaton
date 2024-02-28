# coding=utf-8
import json

class ExperienceItem:
    starts: str
    ends: str
    employer: str
    city: str
    position: str
    description: str


class EducationItem:
    year: str
    organization: str
    faculty: str
    specialty: str
    result: str
    education_type: str
    education_level: str

class Resume:
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


class Vacancy:
    uuid: str
    name: str
    keywords: str
    description: str
    comment: str
    failed_resumes: list[Resume]
    confirmed_resumes: list[Resume]


def parse_json_to_structure(json_data: dict) -> Vacancy:
    vacancy = Vacancy()
    vacancy.uuid = json_data['vacancy']['uuid']
    vacancy.name = json_data['vacancy']['name']
    vacancy.keywords = json_data['vacancy']['keywords']
    vacancy.description = json_data['vacancy']['description']
    vacancy.comment = json_data['vacancy']['comment']
    vacancy.failed_resumes = parse_resumes(json_data['failed_resumes'])
    vacancy.confirmed_resumes = parse_resumes(json_data['confirmed_resumes'])
    return vacancy


def parse_resumes(resumes: list[dict]) -> list[Resume]:
    result = []
    for resume in resumes:
        r = Resume()
        r.uuid = resume['uuid']
        r.first_name = resume['first_name']
        r.last_name = resume['last_name']
        r.birth_date = resume['birth_date']
        r.country = resume['country']
        r.city = resume['city']
        r.about = resume['about']
        r.key_skills = resume['key_skills']
        r.experienceItem = parse_experience_items(resume['experienceItem']) if 'experienceItem' in resume and resume[
            'experienceItem'] else []
        r.educationItem = parse_education_items(resume['educationItem']) if 'educationItem' in resume and resume[
            'educationItem'] else []
        r.languageItems = resume['languageItems'] if 'languageItems' in resume else []
        result.append(r)
    return result


def parse_experience_items(experience_items: list[dict]) -> list[ExperienceItem]:
    result = []
    for item in experience_items:
        e = ExperienceItem()
        e.starts = item['starts']
        e.ends = item['ends']
        e.employer = item['employer']
        e.city = item['city']
        e.position = item['position']
        e.description = item['description']
        result.append(e)
    return result


def parse_education_items(education_items: list[dict]) -> list[EducationItem]:
    result = []
    for item in education_items:
        e = EducationItem()
        e.year = item['year']
        e.organization = item['organization']
        e.faculty = item['faculty']
        e.specialty = item['specialty']
        e.result = item['result']
        e.education_type = item['education_type']
        e.education_level = item['education_level']
        result.append(e)
    return result


def parse_file(file_path: str) -> list[Vacancy]:
    with open(file_path, 'r') as file:
        json_str = json.load(file)
        return list(map(parse_json_to_structure, json_str))


def main():
    vacancies = parse_file('case_2_data_for_members.json')
    print(vacancies[0].failed_resumes[0].first_name)
    print(vacancies[0].confirmed_resumes[0].first_name)


if __name__ == "__main__":
    main()