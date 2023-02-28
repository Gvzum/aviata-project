from typing import Type

from .handler import BaseHandler
from .provider_a import AProviderHandler
from .provider_b import BProviderHandler


def get_all_handler() -> list[Type[BaseHandler]]:
    return [
        AProviderHandler,
        BProviderHandler,
    ]
