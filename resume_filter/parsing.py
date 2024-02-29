import json

from pydantic import TypeAdapter

from resume_filter import settings
from resume_filter.models import CandidateSelection, SortedCandidateSelection

FILENAME: str = "case_2_data_for_members.json"
FILENAME2: str = "case_2_reference_without_resume_sorted.json"


def load_train() -> list[SortedCandidateSelection]:
    file_path: str = f"{settings.DATA_DIR}/{FILENAME}"
    with open(file_path, "r") as f:
        json_dict: dict = json.load(f)
    return TypeAdapter(list[SortedCandidateSelection]).validate_python(json_dict)


def load_test() -> CandidateSelection:
    file_path: str = f"{settings.DATA_DIR}/{FILENAME2}"
    with open(file_path, "r") as f:
        json_dict: dict = json.load(f)
    return TypeAdapter(CandidateSelection).validate_python(json_dict)


if __name__ == "__main__":
    sorted_candidate_selection: list[SortedCandidateSelection] = load_train()
    candidate_selection: CandidateSelection = load_test()
    print(sorted_candidate_selection)
    print(candidate_selection)
