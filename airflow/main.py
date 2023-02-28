from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import deps
from tasks import handle_service_request
from crud import create_service_request, get_service_request, async_get_service_request
from utils import convert_currency

app = FastAPI()


@app.post('/search')
async def search(db: AsyncSession = Depends(deps.get_db)):
    service_request = await create_service_request(db)
    handle_service_request.apply_async(args=[service_request.uuid])

    return {
        'search_id': service_request.uuid
    }


@app.get('/results/{search_id}/{currency}')
async def results(
        *,
        db: AsyncSession = Depends(deps.get_db),
        search_id: str,
        currency: str,
):
    service_request = await async_get_service_request(db, service_request_uuid=search_id)
    items = await convert_currency(
        db,
        service_request.items,
        currency,
    )
    return {
        'search_id': service_request.uuid,
        'status': service_request.status,
        'items': items,
    }
