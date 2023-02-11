from fastapi import Depends, Response, APIRouter
from fastapi import status

from services.db import DBService, get_db_service


router = APIRouter()


@router.get(
    '/ping',
    description='Returns information about the availability status of the database',
    summary='Status of the database',
    status_code=status.HTTP_200_OK
)
async def ping(db_service: DBService = Depends(get_db_service)) -> Response:
    if await db_service.ping_db():
        return Response(status_code=status.HTTP_200_OK)
    return Response(status_code=status.HTTP_400_BAD_REQUEST)
