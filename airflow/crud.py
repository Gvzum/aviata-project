from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, joinedload

from db.models import ServiceRequest, Currency


async def create_service_request(db: AsyncSession) -> ServiceRequest:
    service_request = ServiceRequest()
    db.add(service_request)
    await db.commit()
    await db.refresh(service_request)

    return service_request


async def async_get_service_request(
        db: AsyncSession,
        *,
        service_request_uuid: str,
) -> ServiceRequest:
    query = (
        select(ServiceRequest)
        .options(
            joinedload(ServiceRequest.items)
        )
        .filter(ServiceRequest.uuid == service_request_uuid)
    )
    obj = await db.execute(query)
    print(f'{obj = } kkkkk')
    return obj.scalars().first()


def get_service_request(
        db: Session,
        service_request_uuid: str,
        with_items: bool = False,
) -> ServiceRequest:
    query = (
        select(ServiceRequest)
        .filter(ServiceRequest.uuid == service_request_uuid)
    )
    obj = db.execute(query)

    return obj.scalars().first()


def update_or_create_currency_data(
        *,
        db: Session,
        data: list,
):
    for curr_data in data:
        query = (
            select(Currency)
            .filter(Currency.title == curr_data.get('title'))
        )
        currency = db.execute(query).scalars().first()

        if not currency:
            db.add(
                Currency(
                    title=curr_data.get('title'),
                    full_name=curr_data.get('full_name'),
                    description=curr_data.get('description'),
                    quant=curr_data.get('quant'),
                    index=curr_data.get('index'),
                    change=curr_data.get('change'),
                )
            )
        else:
            currency.title = curr_data.get('title')
            currency.full_name = curr_data.get('full_name')
            currency.description = curr_data.get('description')
            currency.quant = curr_data.get('quant')
            currency.index = curr_data.get('index')
            currency.change = curr_data.get('change')

    db.commit()


async def get_currency(
        *,
        db: AsyncSession,
        currency_title: str,
) -> Currency:
    query = (
        select(Currency)
        .filter(Currency.title == currency_title)
    )
    obj = await db.execute(query)

    return obj.scalars().first()
