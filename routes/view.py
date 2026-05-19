from flask import Blueprint, render_template
from services.gas_client import list_records

bp = Blueprint('view', __name__)


@bp.route('/')
def index():
    records = list_records()
    return render_template('index.html', records=records)
