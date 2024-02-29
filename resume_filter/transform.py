from resume_filter import settings
from resume_filter.models import SortedCandidateSelection, Resume, Vacancy
from resume_filter.models.education_item import EducationItem
from resume_filter.parsing import load_train

from datetime import datetime, timedelta, date

import pandas as pd


class TransformedData:
    vacancy_id: str
    vacancy_main_keywords: list[str]
    # vacancy_sub_keywords: list[str]
    resume_id: str
    requested_experience: int
    is_english: bool
    resume_main_keywords: list[str]
    # resume_sub_keywords: list[str]
    edu: list[str]
    resume_experience: int
    target: int


def parse_education_items(education_items: list[EducationItem]) -> str:
    if not education_items or len(education_items) == 0:
        return 'no'
    levels = list(map(lambda x: x.education_level, education_items))
    if 'Высшее' in levels:
        return 'relevant_high'
    return 'courses'


def get_data(vacancy: Vacancy, resume: Resume, target: bool | None) -> dict[str, any]:
    data: TransformedData = TransformedData()
    data.vacancy_id = vacancy.uuid
    vacancy_name: str = vacancy.name.lower()
    vacancy_name_list: list[str] = vacancy_name.split(' ')
    vacancy_name_list = list(filter(lambda x: x != '', vacancy_name_list))
    data.vacancy_main_keywords = vacancy_name_list
    data.resume_id = resume.uuid
    data.requested_experience = vacancy.requested_experience if vacancy.requested_experience else 0
    if resume.languageItems:
        data.is_english = "Английский" in resume.languageItems
    else:
        data.is_english = False
    if resume.key_skills:
        skills_str: str = (resume.key_skills
                           .lower()
                           .replace(';', ',')
                           .replace('(', '')
                           .replace(')', ''))
        skills_list: list[str] = skills_str.split(',')
        skills_map: map[str] = map(lambda x: x.strip(), skills_list)
        skills_map = filter(lambda x: x != '', skills_map)
        data.resume_main_keywords = list(skills_map)
    else:
        data.resume_main_keywords = []
    data.edu = parse_education_items(resume.educationItem)
    if resume.experienceItem and len(resume.experienceItem) > 0:
        carrier_start: date = min(map(lambda x: x.starts, resume.experienceItem))
        if None in map(lambda x: x.ends, resume.experienceItem):
            carrier_end: date = datetime.now().date()
        else:
            carrier_end: date = max(map(lambda x: x.ends, resume.experienceItem))
        delta: timedelta = carrier_end - carrier_start
        data.resume_experience = int(delta.days / 365.25)
    else:
        data.resume_experience = 0
    data.target = target
    return data.__dict__


def get_count_dict(keywords: list[list[str]]) -> dict[str, int]:
    count_dict = {}
    for keyword_list in keywords:
        for keyword in keyword_list:
            if keyword in count_dict:
                count_dict[keyword] += 1
            else:
                count_dict[keyword] = 1
    return count_dict


def process_data(data: pd.DataFrame) -> pd.DataFrame:
    resume_keywords_count_dict = get_count_dict(data['resume_main_keywords'])
    rare_keywords = []
    for keyword, count in resume_keywords_count_dict.items():
        if count < 10:
            rare_keywords.append(keyword)

    # remove from resume_main_keywords rare keywords
    data['resume_main_keywords'] = (data['resume_main_keywords']
                                    .apply(lambda x: list(filter(lambda y: y not in rare_keywords, x))))
    return data


def data_to_output(data: pd.DataFrame) -> pd.DataFrame:
    output = data[
        ['vacancy_id', 'resume_id', 'requested_experience', 'is_english', 'edu', 'target', 'resume_experience']
    ].copy()
    output['vacancy_main_keywords'] = data['vacancy_main_keywords'].apply(lambda x: ' '.join(x))
    output['resume_main_keywords'] = data['resume_main_keywords'].apply(lambda x: ' '.join(x))
    return output


def get_df_from_vacancies(candidate_selections: list[SortedCandidateSelection]) -> pd.DataFrame:
    results = []
    for selection in candidate_selections:
        for resume in selection.failed_resumes:
            result = get_data(selection.vacancy, resume, False)
            results.append(result)
        for resume in selection.confirmed_resumes:
            result = get_data(selection.vacancy, resume, True)
            results.append(result)
    df_results = pd.DataFrame(results)
    return df_results


def main():
    vacancies: list[SortedCandidateSelection] = load_train()
    df = get_df_from_vacancies(vacancies)
    data = process_data(df)
    output = data_to_output(data)
    output_path: str = f"{settings.DATA_DIR}/case_2_results.csv"
    output.to_csv(output_path, index=False)


if __name__ == '__main__':
    main()
