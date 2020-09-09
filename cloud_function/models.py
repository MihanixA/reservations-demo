import typing
import datetime
from pydantic import BaseModel


class Reservation(BaseModel):
    reservation_id: int = None
    description: typing.Optional[typing.Union[bytes, str]] = None
    table_id: int
    dt: datetime.datetime


class Table(BaseModel):
    table_id: int = None
    description: typing.Optional[typing.Union[bytes, str]] = None
    cnt: int


class ReservationCreateRequest(BaseModel):
    dt: datetime.datetime
    cnt: int
    description: typing.Optional[typing.Union[bytes, str]] = None


class ReservationCreateResponse(BaseModel):
    success: bool
    table_id: typing.Optional[int] = None
    reservation_id: typing.Optional[int] = None


class ReservationCancelRequest(BaseModel):
    reservation_id: int


class ReservationCancelResponse(BaseModel):
    success: bool
