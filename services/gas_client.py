import csv
import io
import requests
from config import PHP_ENDPOINT

NYUKA_SHEET_URL = 'https://docs.google.com/spreadsheets/d/1wEg-0TOLjVcmwe30GWBgEF3NUFwQ6YhthbQCe1fhxco/gviz/tq?tqx=out:csv&gid=0'


def fetch_nyuka_schedule() -> dict:
    """品番 → {qty, date} の辞書を返す。取得失敗時は空dict。"""
    try:
        resp = requests.get(NYUKA_SHEET_URL, timeout=10)
        reader = csv.reader(io.StringIO(resp.text))
        next(reader, None)  # ヘッダー行をスキップ
        result = {}
        for row in reader:
            if len(row) < 4:
                continue
            sku  = row[1].strip()   # B列：品番
            qty  = row[2].strip()   # C列：入荷数量
            date = row[3].strip()   # D列：入荷日
            if sku and date:
                result[sku] = {'qty': qty, 'date': date}
        return result
    except Exception:
        return {}


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
