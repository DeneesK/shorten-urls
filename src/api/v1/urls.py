from fastapi import APIRouter, Depends, Response
from fastapi import status

from services.urls import UrlService, get_url_service
from .models import UrlResponse, UrlIn, InfoModel

router = APIRouter()


@router.post(
    '/',
    response_model=UrlResponse,
    description='Get a shortened version of the given URL',
    summary='Create short urls',
    status_code=status.HTTP_201_CREATED
)
async def shorten_url(
    body: UrlIn,
    url_service: UrlService = Depends(get_url_service)
) -> UrlResponse:
    new_url = await url_service.create_shorten_url(body.url)
    return UrlResponse.parse_obj(new_url.__dict__)


@router.get(
    '/{shorten_url_id}',
    description="""The method takes a shortened URL ID
    as a parameter and returns a response with a 307
    code and the original URL in the Location header""",
    summary='Redirect to the original URL',
    status_code=status.HTTP_307_TEMPORARY_REDIRECT
)
async def get_origin_url(
    shorten_url_id: str,
    url_service: UrlService = Depends(get_url_service)
) -> Response:
    url = await url_service.get_by_id(shorten_url_id)
    return Response(headers={'Location': url.original_url}, status_code=status.HTTP_307_TEMPORARY_REDIRECT)


@router.get(
    '/{shorten_url_id}/status',
    response_model=InfoModel,
    description="""The method takes as a parameter
    the identifier of a shortened URL and returns
    information about the number of clicks made on the URL""",
    summary='Return info about numbers of  clicks made on the link URL',
    status_code=status.HTTP_200_OK
)
async def get_url_status(
    shorten_url_id: str,
    url_service: UrlService = Depends(get_url_service)
):
    info = await url_service.get_info(shorten_url_id)
    return InfoModel.parse_obj(info.__dict__)
