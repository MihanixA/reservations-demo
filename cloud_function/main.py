import json
import logging
from config import Config
from storage import Storage as YDBStorage
from controller import Controller
from models import ReservationCreateRequest, ReservationCreateResponse


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

    if event['httpMethod'] == 'POST':
        logging.info('Got ReservationCreateRequest')
        try:
            request = ReservationCreateRequest(**json.loads(event['body']))
            response: ReservationCreateResponse = controller.maybe_make_reservation(request)
            data = json.dumps(response.dict())
        except Exception as e:
            logging.warning(f'ReservationCreateRequest failed due to {repr(e)}')
            status_code = 400
            error = repr(e)
    elif event['httpMethod'] == 'DELETE':
        ...
    elif event['httpMethod'] == 'PUT':
        ...
    elif event['httpMethod'] == 'GET':
        ...

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

