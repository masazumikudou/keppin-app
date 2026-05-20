import requests
from config import PHP_ENDPOINT


def save_records(records: list) -> dict:
    resp = requests.post(
        f'{PHP_ENDPOINT}?action=save',
        json={'records': records},
        timeout=15,
    )
    return resp.json()


def list_records(filters: dict = None) -> list:
    params = {'action': 'list'}
    if filters:
        params.update(filters)
    resp = requests.get(PHP_ENDPOINT, params=params, timeout=15)
    return resp.json().get('records', [])


def delete_store_records(store_name: str, staff_name: str, date: str = '') -> dict:
    resp = requests.post(
        f'{PHP_ENDPOINT}?action=delete_store',
        json={'store_name': store_name, 'staff_name': staff_name, 'date': date},
        timeout=15,
    )
    return resp.json()


def ship_record(record_id) -> dict:
    resp = requests.post(
        f'{PHP_ENDPOINT}?action=ship',
        json={'id': int(record_id)},
        timeout=15,
    )
    return resp.json()
