import json

from pydantic import TypeAdapter

from resume_filter import settings
from resume_filter.models import CandidateSelection, SortedCandidateSelection


FILENAME: str = "case_2_data_for_members.json"
FILENAME2: str = "case_2_reference_without_resume_sorted.json"

file_path: str = f"{settings.DATA_DIR}/{FILENAME}"
file_path2: str = f"{settings.DATA_DIR}/{FILENAME2}"

with open(file_path, 'r') as file:
    json_dict: dict = json.load(file)

with open(file_path2, 'r') as file:
    json_dict2: dict = json.load(file)

sorted_candidate_selection: list[SortedCandidateSelection] = TypeAdapter(
    list[SortedCandidateSelection]
).validate_python(json_dict)

candidate_selection: CandidateSelection = TypeAdapter(CandidateSelection).validate_python(json_dict2)


print(sorted_candidate_selection)
print(candidate_selection)
