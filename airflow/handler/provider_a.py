from urllib.parse import urljoin

from config.settings import settings
from db.models import ItemData
from handler.handler import BaseRESTHandler
from handler.schemas import ItemListSchema
from handler.utils import append_items


class AProviderHandler(BaseRESTHandler):
    url = urljoin(settings.PROVIDER_A, '/search')
    method = 'POST'
    validate_schema = ItemListSchema

    def _save(self, data: list):
        append_items(
            db=self._db,
            service_request=self._service_request,
            data=data
        )
        # items = []
        # for item in data:
        #     item.append(
        #         ItemData(
        #             service_request=self._service_request,
        #             flights=item.get('flights'),
        #             refundable=item.get('refundable'),
        #             validating_airline=item.get('validating_airline'),
        #             pricing=item.get('pricing'),
        #         )
        #     )
        # self._db.add_all(items)
        # self._db.commit()

    def _parse(self, data: dict):
        if not data:
            raise Exception(
                'Data to parse is empty'
            )
        return data
