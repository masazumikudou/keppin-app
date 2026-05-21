from flask import Blueprint, render_template
from services.gas_client import list_records, fetch_nyuka_schedule
from services.staff_master import load_staff_by_name
from config import TN_APP_URL

bp = Blueprint('view', __name__)

_NYUKA_BADGE_COLORS = [
    {'bg': '#ffebee', 'text': '#c62828'},  # 赤
    {'bg': '#e3f2fd', 'text': '#1565c0'},  # 青
    {'bg': '#e8f5e9', 'text': '#2e7d32'},  # 緑
    {'bg': '#fff3e0', 'text': '#e65100'},  # オレンジ
    {'bg': '#f3e5f5', 'text': '#6a1b9a'},  # 紫
]


def _nyuka_badge(nyuka: dict) -> dict:
    dates = [v['date'] for v in nyuka.values() if isinstance(v, dict) and v.get('date')]
    if not dates:
        return {}
    def parse_md(d):
        try:
            m, day = d.split('/')
            return (int(m), int(day))
        except Exception:
            return (0, 0)
    latest = max(dates, key=parse_md)
    color = _NYUKA_BADGE_COLORS[hash(latest) % len(_NYUKA_BADGE_COLORS)]
    return {'date': latest, 'bg': color['bg'], 'text': color['text']}


@bp.route('/')
def index():
    records = list_records()
    staff_list = list(load_staff_by_name().keys())
    nyuka = fetch_nyuka_schedule()
    nyuka_badge = _nyuka_badge(nyuka)
    return render_template('index.html', records=records, staff_list=staff_list, tn_app_url=TN_APP_URL, nyuka=nyuka, nyuka_badge=nyuka_badge)
