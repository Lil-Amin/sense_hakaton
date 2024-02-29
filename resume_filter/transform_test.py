from resume_filter import settings
from resume_filter.models import SortedCandidateSelection, Resume, Vacancy, CandidateSelection, resume
from resume_filter.models.education_item import EducationItem
from resume_filter.parsing import load_train, load_test

from datetime import datetime, timedelta, date

import pandas as pd

from resume_filter.transform import get_data


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


def get_df_from_vacancies(candidate_selection: CandidateSelection) -> pd.DataFrame:
    results = []
    for resume in candidate_selection.resumes:
        result = get_data(candidate_selection.vacancy, resume, None)
        results.append(result)
    df_results = pd.DataFrame(results)
    return df_results


def main():
    vacancies: CandidateSelection = load_test()
    df = get_df_from_vacancies(vacancies)
    data = process_data(df)
    output = data_to_output(data)
    output_path: str = f"{settings.DATA_DIR}/case_2_results_test.csv"
    output.to_csv(output_path, index=False)


if __name__ == '__main__':
    main()
