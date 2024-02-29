from resume_filter import settings
from resume_filter.models import CandidateSelection
from resume_filter.parsing import load_test

import pandas as pd

from resume_filter.transform import get_data, process_data, data_to_output


def get_df_from_test_vacancies(candidate_selection: CandidateSelection) -> pd.DataFrame:
    results = []
    for resume in candidate_selection.resumes:
        result = get_data(candidate_selection.vacancy, resume, None)
        results.append(result)
    df_results = pd.DataFrame(results)
    return df_results


def main():
    vacancies: CandidateSelection = load_test()
    df = get_df_from_test_vacancies(vacancies)
    data = process_data(df)
    output = data_to_output(data)
    output_path: str = f"{settings.DATA_DIR}/case_2_results_test.csv"
    output.to_csv(output_path, index=False)


if __name__ == '__main__':
    main()
