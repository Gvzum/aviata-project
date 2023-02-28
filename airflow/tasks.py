import datetime
import logging
from abc import ABC, abstractmethod
from typing import Type
from urllib.parse import urljoin

import requests
from celery import shared_task, Task, group, chain
from lxml.etree import fromstring

from config.settings import settings
from crud import get_service_request, update_or_create_currency_data
from db.engine import SessionSync
from db.enums import StatusCode
from handler import get_all_handler
from handler.provider_a import AProviderHandler


@shared_task
def set_status_of_service_request(
        service_request_uuid: str,
        status: str
):
    with SessionSync() as db:
        service_request = get_service_request(db, service_request_uuid)
        service_request.status = status
        db.commit()


class HandleServiceRequestTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        service_request_uuid = self.request.get('service_request_uuid')
        set_status_of_service_request.delay(
            service_request_uuid,
            StatusCode.ERROR.name,
        )

    def on_success(self, retval, task_id, args, kwargs):
        service_request_uuid = self.request.get('service_request_uuid')
        handler_idx = self.request.get('handler_idx')
        status = StatusCode.FINISHED.name
        if handler_idx == 0:
            status = StatusCode.IN_PROGRESS.name

        set_status_of_service_request.delay(
            service_request_uuid,
            status,
        )


@shared_task(
    bind=True,
    base=HandleServiceRequestTask,
)
def call_handler_service_request(
        task_: HandleServiceRequestTask,
        idx: int,
        service_request_uuid: str,
):
    logging.info('Call handler service request')
    logging.info(f'{idx = }')
    with SessionSync() as db:
        task_.request.update(service_request_uuid=service_request_uuid)
        task_.request.update(handler_idx=idx)
        service_request = get_service_request(db, service_request_uuid)
        handler = get_all_handler()[idx](
            db=db,
            service_request=service_request
        )
        handler()
        logging.info(f'{db.is_active = }')
        db.commit()


@shared_task
def handle_service_request(
        service_request_uuid: str
):
    logging.info('Run task Service Request')
    logging.info(f'{service_request_uuid = }')
    chain(*[
        call_handler_service_request.si(
            idx,
            service_request_uuid,
        ) for idx in range(len(get_all_handler()))
    ]).delay()


@shared_task
def update_currency():
    logging.info('Run task Update Currency')

    def parse(data):
        logging.info('Parse currency data')
        root = fromstring(data)
        return [
            {
                'full_name': currency_data.findtext('fullname'),
                'title': currency_data.findtext('title'),
                'description': currency_data.findtext('description'),
                'quant': currency_data.findtext('quant'),
                'index': currency_data.findtext('index'),
                'change': currency_data.findtext('change'),
            } for currency_data in root.xpath('item')
        ]

    with SessionSync() as db:
        today = datetime.date.today()
        url = urljoin(settings.NATIONAL_BANK, f'/rss/get_rates.cfm?fdate={today.strftime("%d.%m.%Y")}')
        response = requests.get(url)
        logging.info(
            f'{response.status_code = } '
            f'{response.url = } '
            f'{response.content = }'
        )

        parsed_data = parse(response.content)
        update_or_create_currency_data(
            db=db,
            data=parsed_data,
        )
