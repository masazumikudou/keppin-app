from flask import Blueprint, request, jsonify
from services.gas_client import save_records
from services.slack_client import notify
from services.staff_master import load_staff_by_name
import datetime

bp = Blueprint('shortage', __name__)


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
        items      = store.get('items', [])

        # GAS保存用レコードを組み立て
        for item in items:
            records.append({
                'date':           date,
                'aggregate_name': aggregate,
                'store_name':     store_name,
                'staff_name':     staff_name,
                'sku':            item.get('sku', ''),
                'color':          item.get('color', ''),
                'quantity':       item.get('quantity', 0),
                'is_shortage':    item.get('is_shortage', False),
            })

        # Slack通知
        staff_info = staff_master.get(staff_name, {})
        member_id  = staff_info.get('slack_member_id', '')
        ok = notify(member_id, date_str, store_name)
        if ok:
            sent += 1
        else:
            errors.append(f'{store_name}: Slack通知失敗')

    # GASに一括保存
    try:
        save_records(records)
    except Exception as e:
        return jsonify({'success': False, 'error': f'データ保存失敗: {e}'}), 502

    if errors:
        return jsonify({'success': False, 'error': ', '.join(errors), 'sent': sent})
    return jsonify({'success': True, 'sent': sent})
