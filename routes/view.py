from flask import Blueprint, render_template
from services.gas_client import list_records, fetch_nyuka_schedule
from services.staff_master import load_staff_by_name
from config import TN_APP_URL

bp = Blueprint('view', __name__)

_NYUKA_BADGE_COLORS = [
    {'bg': '#221010', 'text': '#e87070'},  # 赤
    {'bg': '#0d1926', 'text': '#6aaad4'},  # 青
    {'bg': '#0d1f14', 'text': '#62b87a'},  # 緑
    {'bg': '#221808', 'text': '#d49040'},  # オレンジ
    {'bg': '#1a1028', 'text': '#b07ed4'},  # 紫
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
    parts = latest.split('/')
    color_idx = (int(parts[0]) * 31 + int(parts[1])) % len(_NYUKA_BADGE_COLORS)
    color = _NYUKA_BADGE_COLORS[color_idx]
    return {'date': latest, 'bg': color['bg'], 'text': color['text']}


@bp.route('/')
def index():
    records = list_records()
    staff_list = list(load_staff_by_name().keys())
    nyuka = fetch_nyuka_schedule()
    nyuka_badge = _nyuka_badge(nyuka)
    return render_template('index.html', records=records, staff_list=staff_list, tn_app_url=TN_APP_URL, nyuka=nyuka, nyuka_badge=nyuka_badge)
