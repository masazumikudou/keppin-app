import requests
from config import OS2_PHP_ENDPOINT


def save_order(store_name: str, staff_name: str, staff_code: str, items: list) -> dict:
    os2_items = [
        {
            'hinban':   item['sku'],
            'iro':      item.get('color', ''),
            'quantity': int(item.get('quantity', 0)),
        }
        for item in items
    ]
    payload = {
        'source':     'kekkin',
        'store_name': store_name,
        'staff_name': staff_name,
        'staff_code': staff_code,
        'items':      os2_items,
        'status':     'new',
    }
    resp = requests.post(
        f'{OS2_PHP_ENDPOINT}?action=save',
        json=payload,
        timeout=15,
    )
    return resp.json()
