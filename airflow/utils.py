import logging

from sqlalchemy.ext.asyncio import AsyncSession

from crud import get_currency
from db.models import ItemData


async def convert_currency(
        db: AsyncSession,
        items: list[ItemData],
        currency_title: str
):
    async def convert_price_currency(price: dict):
        print(price)
        price_currency = price.get('currency')
        print(price_currency)
        if currency_title == price_currency:
            return price
        # print(
        #     f'{price_currency = } '
        #     f'{currency_title = }'
        # )

        total = float(price.get('total'))
        base = float(price.get('base'))
        # print(
        #     f'{total = } '
        #     f'{base = }'
        # )

        first_convert = await get_currency(
            db=db,
            currency_title=currency_title,
        )
        if first_convert and first_convert.title != 'KZT':
            total *= first_convert.description
            base *= first_convert.description

        second_convert = await get_currency(
            db=db,
            currency_title=price_currency
        )
        if second_convert and second_convert.title != 'KZT':
            total /= second_convert.description
            base /= second_convert.description

        return {
            'taxes': price.get('taxes'),
            'total': total,
            'base': base,
            'currency': currency_title,
        }

    return [
        {
            'flights': item.flights,
            'refundable': item.refundable,
            'validating_airline': item.validating_airline,
            'pricing': await convert_price_currency(item.pricing)
        } for item in items
    ]
