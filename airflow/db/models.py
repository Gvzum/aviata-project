from sqlalchemy import Integer, Column, String, Float, ForeignKey, Boolean, JSON, Enum, ARRAY
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression

from db.enums import StatusCode
from db.utils import generate_uuid

Base = declarative_base()


class Currency(Base):
    __tablename__ = 'currency'

    title = Column(String, primary_key=True)

    full_name = Column(String(255))
    description = Column(Float)
    quant = Column(Integer, server_default='0')
    index = Column(String)
    change = Column(Float)


class ItemData(Base):
    __tablename__ = 'item_data'

    id = Column(Integer, primary_key=True)

    flights = Column(JSONB, server_default='{}')
    refundable = Column(Boolean(), nullable=False, server_default=expression.false())
    validating_airline = Column(String)
    pricing = Column(JSONB, server_default='{}')

    service_request_uuid = Column(String, ForeignKey('service_request.uuid', ondelete='CASCADE'))
    service_request = relationship('ServiceRequest', back_populates='items')


class ServiceRequest(Base):
    __tablename__ = 'service_request'

    uuid = Column(String, name="uuid", primary_key=True, default=generate_uuid)

    status = Column(String, default=StatusCode.PENDING.name)
    items = relationship('ItemData', back_populates='service_request')
