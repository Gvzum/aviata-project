from typing import Optional

from pydantic import BaseModel, Field


class Airport(BaseModel):
    at: str
    airport: str


class Segment(BaseModel):
    operating_airline: str
    marketing_airline: str
    flight_number: str
    equipment: Optional[str]
    dep: Airport
    arr: Airport
    baggage: str


class FlightData(BaseModel):
    duration: int
    segments: list[Segment]


class Price(BaseModel):
    total: float
    base: float
    taxes: float
    currency: str


class ItemData(BaseModel):
    flights: list[FlightData]
    refundable: bool
    validating_airline: str
    pricing: dict


class ItemListSchema(BaseModel):
    __root__: list[ItemData]
