import logging
from abc import abstractmethod, ABC
from typing import Optional, Type, Any, Union

from pydantic import BaseModel
from sqlalchemy.orm import Session
import requests

from db.models import ServiceRequest


class BaseHandler(ABC):

    @property
    @abstractmethod
    def url(self) -> str:
        ...

    @property
    @abstractmethod
    def method(self) -> str:
        ...

    @property
    @abstractmethod
    def validate_schema(self) -> Optional[Type["BaseModel"]]:
        ...

    @abstractmethod
    def _call(self) -> Any:
        ...

    @abstractmethod
    def _save(self, data):
        ...

    @abstractmethod
    def _parse(self, data: Any) -> Union[list, dict]:
        ...

    def __init__(self, db: Session, service_request: "ServiceRequest"):
        logging.info(
            f'{service_request = }'
        )
        self._db = db
        self._service_request = service_request

    def __call__(self) -> Any:
        logging.info('Call Handler')
        response_data = self._call()
        # parsed_data = self._parse(response_data)
        validated_data = self._validate_response(response_data)
        self._save(validated_data)
        logging.info('After commit')
        self._db.commit()

    def _validate_response(self, data_to_validate):
        logging.info(f'Validate response')
        self.validate_schema.parse_obj(data_to_validate)
        return data_to_validate


class BaseXMLHandler(BaseHandler, ABC):
    def _call(self):
        response = requests.request(
            self.method,
            self.url,
        )
        return self._parse(response.content)


class BaseRESTHandler(BaseHandler, ABC):
    def _call(self):
        response = requests.request(
            self.method,
            self.url,
        )
        logging.info(
            f'{response.status_code = } '
            f'{response.url = } '
        )
        return self._parse(response.json())


