import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from db import db
from core.config import app_settings
from api.v1 import main_router


app = FastAPI(
    title=app_settings.app_title,
    description=app_settings.app_description,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json'
)


@app.middleware('http')
async def validate_ip(request: Request, call_next):
    ip = str(request.client.host)
    if ip in app_settings.blacklist:
        data = {'message': f'IP {ip} is not allowed to access this resource.'}
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=data)
    return await call_next(request)


@app.on_event('startup')
async def on_startup():
    engine = create_async_engine(app_settings.database_dsn, echo=True, future=True)
    db.async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@app.on_event('shutdown')
async def on_shutdown():
    db.async_session.close_all()


app.include_router(main_router, prefix='/api/v1')


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        reload=True
    )
