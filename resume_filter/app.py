import typing

from litestar import Litestar, get, post, MediaType
from litestar.datastructures import UploadFile
from litestar.enums import RequestEncodingType
from litestar.params import Body
from pandas import DataFrame

from resume_filter import settings
from resume_filter.models import CandidateSelection
from catboost import CatBoostClassifier

from resume_filter.parsing import load_test
from resume_filter.transform_test import get_df_from_test_vacancies
from resume_filter.transform import process_data, data_to_output

NUM_MODELS = 5


def model_inference(candidate_selection: CandidateSelection) -> list[str]:
    input: DataFrame = get_df_from_test_vacancies(candidate_selection)
    data: DataFrame = process_data(input)
    output: DataFrame = data_to_output(data)
    output = output.drop(columns=['target', 'vacancy_id', 'resume_id', 'resume_description'])
    for fold in range(0, NUM_MODELS):
        # Specify the file path from which you want to load the model
        dir_path = settings.NOTEBOOK_DIR
        model_path = f'{dir_path}/catboost_model_fold_new_{fold}.cbm'

        # Load the model from the specified file path
        inference_model: CatBoostClassifier = CatBoostClassifier()
        inference_model.load_model(model_path)

        # Make predictions on the validation set
        preds_proba = inference_model.predict_proba(output[inference_model.feature_names_])

        if fold == 0:
            preds_proba_total = preds_proba
        else:
            preds_proba_total += preds_proba

    preds_proba_total = preds_proba_total / NUM_MODELS
    preds = preds_proba_total[:, 1]
    preds = preds > 0.5
    input['target'] = preds
    ids = input[input['target']]['resume_id'].tolist()
    return ids


@get("/")
def hello() -> str:
    return "Hello!"


@post("/filter_resumes", sync_to_thread=False)
def filter_resumes(data: CandidateSelection) -> list[str]:
    ids: list[str] = model_inference(data)

    return ids


@post("/filter_resumes_file", media_type=MediaType.JSON, sync_to_thread=False)
def filter_resumes_file(
        data: typing.Annotated[UploadFile, Body(media_type=RequestEncodingType.MULTI_PART)]
) -> list[str]:
    content: bytes = data.file.read()
    candidate_selection: CandidateSelection = CandidateSelection.model_validate_json(content)
    ids: list[str] = model_inference(candidate_selection)

    return ids


app: Litestar = Litestar([hello, filter_resumes, filter_resumes_file])


if __name__ == "__main__":
    test_data = load_test()
    print(model_inference(test_data))