import typing
import logging
from storage import Storage
from models import (
    ReservationCreateResponse,
    ReservationCreateRequest,
    ReservationCancelRequest,
    ReservationCancelResponse,
    Table,
    Reservation
)


class Controller(object):

    __slots__ = ('_storage',)

    def __init__(self, storage: Storage):
        self._storage = storage

    def _find_available_table_id(
        self, request: ReservationCreateRequest
    ) -> typing.Optional[int]:
        table_ids = set(self._storage.list_table_ids(cnt=request.cnt))
        reserved_table_ids = set(self._storage.find_reserved_table_ids(
            cnt=request.cnt, dt=request.dt
        ))
        for table_id in table_ids.difference(reserved_table_ids):
            return table_id

    def maybe_make_reservation(self, request: ReservationCreateRequest) -> ReservationCreateResponse:
        table_id = self._find_available_table_id(request)
        if table_id is None:
            logging.warning('reservation failed')
            return ReservationCreateResponse(success=False)
        reservation_id = self._storage.save_reservation(
            dt=request.dt, table_id=table_id,
            cnt=request.cnt, description=request.description
        )
        logging.warning(f'reservation {reservation_id} succeeded')
        return ReservationCreateResponse(
            success=True,
            reservation_id=reservation_id,
            table_id=table_id
        )
