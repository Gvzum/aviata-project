from datetime import datetime
from urllib.parse import urljoin

from lxml.etree import fromstring

from config.settings import settings
from handler.handler import BaseXMLHandler, BaseRESTHandler
from handler.schemas import ItemListSchema, ItemData
from handler.utils import append_items


class BProviderHandler(BaseXMLHandler):
    url = urljoin(settings.PROVIDER_B, '/search')
    method = 'POST'
    validate_schema = ItemListSchema
    namespace_b = {'b': 'http://schemas.datacontract.org/2004/07/SiteCity.Avia.Common.Avia'}
    namespace_a = {'a': 'http://schemas.datacontract.org/2004/07/SiteCity.Avia.Search'}

    def _save(self, data: list):
        append_items(
            db=self._db,
            service_request=self._service_request,
            data=data
        )

    def _parse_flight(self, flight_data):
        data = []

        def _parse_airport_time(airport_data):
            return {
                'at': airport_data.findtext('.//b:Date', namespaces=self.namespace_b),
                'airport': airport_data.findtext('.//b:Iata', namespaces=self.namespace_b),
            }

        for flight in flight_data:
            segments = [
                {
                    'operating_airline': flight.findtext('.//b:OperatingAirline', namespaces=self.namespace_b),
                    'marketing_airline': flight.findtext('.//b:MarketingAirline', namespaces=self.namespace_b),
                    'flight_number': flight.findtext('.//b:FlightNum', namespaces=self.namespace_b),
                    'equipment': flight.findtext('.//b:AirCraft', namespaces=self.namespace_b),
                    'dep': _parse_airport_time(flight.find('.//b:Departure', namespaces=self.namespace_b)),
                    'arr': _parse_airport_time(flight.find('.//b:Arrival', namespaces=self.namespace_b)),
                    'baggage': flight.findtext('.//b:Baggage/b:BaggageType', namespaces=self.namespace_b),
                }
            ]
            data.append(
                {
                    'duration': flight.findtext('.//b:FlightMinutes', namespaces=self.namespace_b),
                    'segments': segments
                }
            )

        return data

    def _parse_items(self, items: list, currency: str):
        data = []

        for item in items:
            print(item.xpath('.//b:OfferSegment', namespaces=self.namespace_b))
            data.append(
                {
                    'flights': self._parse_flight(item.xpath('.//b:OfferSegment', namespaces=self.namespace_b)),
                    'refundable': item.findtext('.//b:Rph', namespaces=self.namespace_b) == '1',
                    'validating_airline': item.findtext('.//b:ValidatingAirline', namespaces=self.namespace_b),
                    'pricing': {
                        'total': item.findtext('.//a:TotalPrice', namespaces=self.namespace_a),
                        'base': item.find('.//a:TariffInfo', namespaces=self.namespace_a).findtext('.//b:AdultBasePrice', namespaces=self.namespace_b),
                        'taxes': item.findtext('.//a:Rating', namespaces=self.namespace_a),
                        'currency': currency,
                    }
                }
            )
        return data

    def _parse(self, data):
        if not data:
            raise Exception(
                'Data to parse is empty'
            )

        root = fromstring(data)

        return self._parse_items(
            # items=root.xpath("//*[local-name() = 'FlightData']"),
            items=root.xpath('.//a:FlightData', namespaces=self.namespace_a),
            currency=root.findtext('.//Currency'),
        )
