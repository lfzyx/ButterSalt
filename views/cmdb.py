from flask import Blueprint
from flask_login import login_required
from flask import render_template


cmdb = Blueprint('cmdb', __name__, url_prefix='/cmdb')


@cmdb.route('/')
@login_required
def index():
    return render_template('cmdb/cmdb.html')
