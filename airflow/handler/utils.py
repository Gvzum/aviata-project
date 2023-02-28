from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import ServiceRequest, ItemData, Currency


def append_items(
        *,
        db: Session,
        service_request: ServiceRequest,
        data: list,
):
    items = []
    for item in data:
        items.append(
            ItemData(
                service_request=service_request,
                flights=item.get('flights'),
                refundable=item.get('refundable'),
                validating_airline=item.get('validating_airline'),
                pricing=item.get('pricing'),
            )
        )

    db.add_all(items)
    db.commit()
