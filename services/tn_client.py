import requests
from config import TN_APP_URL


def send_order(store_name: str, tantosha: str, store_code: str,
               date: str, items: list, biko: str = '') -> dict:
    if not TN_APP_URL:
        return {'status': 'skipped', 'reason': 'TN_APP_URL not configured'}

    cart = {}
    for i, item in enumerate(items):
        key = f"{item['sku']}_{item.get('color', '')}_{i}"
        cart[key] = {
            'hinban':   item['sku'],
            'iro':      item.get('color', ''),
            'quantity': int(item.get('quantity', 0)),
        }

    payload = {
        'store_name': store_name,
        'tantosha':   tantosha,
        'store_code': store_code,
        'juno_code':  store_code,
        'date':       date,
        'cart':       cart,
        'biko':       biko,
    }
    resp = requests.post(
        f'{TN_APP_URL}/api/send_order',
        json=payload,
        timeout=30,
    )
    return resp.json()
