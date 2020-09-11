import json
import logging
from config import Config
from storage import Storage as YDBStorage
from controller import Controller
from models import (
    ReservationCreateRequest,
    ReservationCreateResponse,
    ReservationCancelRequest,
    ReservationCancelResponse
)


def handler(event, _):
    ydb_storage = YDBStorage(
        endpoint=Config.ydb_endpoint(),
        database=Config.ydb_database(),
        path=Config.ydb_path()
    )
    controller = Controller(ydb_storage)

    status_code = 200
    error = ''
    data = ''

    if event['httpMethod'] == 'GET':
        logging.info('Got ReservationCreateRequest')
        try:
            params = event['queryStringParameters']
            action = params.pop('action')
            if action == 'create':
                request = ReservationCreateRequest(**json.loads(params))
                response: ReservationCreateResponse = controller.maybe_create_reservation(request)
                data = json.dumps(response.dict())
            elif action == 'cancel':
                request = ReservationCancelRequest(**json.loads(params))
                response: ReservationCancelResponse = controller.maybe_cancel_reservation(request)
                data = json.dumps(response.dict())
        except Exception as e:
            logging.warning(f'ReservationCreateRequest failed due to {repr(e)}')
            status_code = 400
            error = repr(e)
    else:
        status_code = 400
        error = 'invalid http method'

    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
        },
        'body': json.dumps({
            'data': data,
            'error': error
        })
    }

