from flask import Blueprint, render_template
from services.gas_client import list_records
from services.staff_master import load_staff_by_name
from config import TN_APP_URL

bp = Blueprint('view', __name__)


@bp.route('/')
def index():
    records = list_records()
    staff_list = list(load_staff_by_name().keys())
    return render_template('index.html', records=records, staff_list=staff_list, tn_app_url=TN_APP_URL)
