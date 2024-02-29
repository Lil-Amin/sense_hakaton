import typing

from litestar import Litestar, get, post, MediaType
from litestar.datastructures import UploadFile
from litestar.enums import RequestEncodingType
from litestar.params import Body

from resume_filter.models import CandidateSelection


def model_inference(candidate_selection: CandidateSelection) -> list[str]:
    # dummy inference
    ids: list[str] = [resume.uuid for resume in candidate_selection.resumes]

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
