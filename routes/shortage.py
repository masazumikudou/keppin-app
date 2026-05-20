from flask import Blueprint, request, jsonify
from services.gas_client import save_records, ship_record, delete_store_records
from services.slack_client import notify
from services.staff_master import load_staff_by_name
import datetime

bp = Blueprint('shortage', __name__)


@bp.route('/api/shortage/ship', methods=['POST'])
def ship():
    data       = request.get_json(force=True)
    ids        = data.get('ids') or ([data.get('id')] if data.get('id') else [])
    items      = data.get('items', [])
    store_name = data.get('store_name', '')
    staff_name = data.get('staff_name', '')
    store_code = data.get('store_code', '')
    date       = data.get('date', datetime.date.today().isoformat())

    if not ids:
        return jsonify({'success': False, 'error': 'idが空です'}), 400

    # DB を出荷済みに更新
    for record_id in ids:
        try:
            ship_record(record_id)
        except Exception:
            pass

    result = {'success': True, 'shipped': len(ids)}

    # 出荷品番がある場合は OS2 登録 + TN メール送信
    if items and store_name:
        try:
            from services.os2_client import save_order
            os2_res = save_order(store_name, staff_name, store_code, items)
            result['os2'] = os2_res
        except Exception as e:
            result['os2_error'] = str(e)

        try:
            from services.tn_client import send_order
            tn_res = send_order(store_name, staff_name, store_code, date, items)
            result['tn'] = tn_res
        except Exception as e:
            result['tn_error'] = str(e)

    return jsonify(result)


@bp.route('/api/shortage/delete_store', methods=['POST'])
def delete_store():
    data       = request.get_json(force=True)
    store_name = data.get('store_name', '')
    staff_name = data.get('staff_name', '')
    date       = data.get('date', '')
    if not store_name or not staff_name:
        return jsonify({'success': False, 'error': 'store_name/staff_nameが空です'}), 400
    result = delete_store_records(store_name, staff_name, date)
    return jsonify(result)


@bp.route('/api/shortage/register', methods=['POST'])
def register():
    data         = request.get_json(force=True)
    aggregate    = data.get('aggregate_name', '')
    date         = data.get('date', datetime.date.today().isoformat())
    date_str     = data.get('date_str', date)
    stores       = data.get('stores', [])

    if not stores:
        return jsonify({'success': False, 'error': '店舗データがありません'}), 400

    staff_master = load_staff_by_name()
    records      = []
    errors       = []
    sent         = 0

    for store in stores:
        store_name = store.get('store_name', '')
        staff_name = store.get('staff_name', '')
        store_code = store.get('store_code', '')
        items      = store.get('items', [])

        for item in items:
            records.append({
                'date':           date,
                'aggregate_name': aggregate,
                'store_name':     store_name,
                'staff_name':     staff_name,
                'store_code':     store_code,
                'sku':            item.get('sku', ''),
                'color':          item.get('color', ''),
                'quantity':       item.get('quantity', 0),
                'is_shortage':    item.get('is_shortage', False),
            })

        staff_info = staff_master.get(staff_name, {})
        member_id  = staff_info.get('slack_member_id', '')
        ok = notify(member_id, date_str, store_name)
        if ok:
            sent += 1
        else:
            errors.append(f'{store_name}: Slack通知失敗')

    try:
        save_records(records)
    except Exception as e:
        return jsonify({'success': False, 'error': f'データ保存失敗: {e}'}), 502

    if errors:
        return jsonify({'success': False, 'error': ', '.join(errors), 'sent': sent})
    return jsonify({'success': True, 'sent': sent})
