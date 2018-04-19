from flask import render_template, redirect, url_for, flash, Blueprint

from flask_login import login_required
from ... import salt


dashboard = Blueprint('dashboard', __name__)


@dashboard.before_request
@login_required
def before_request():
    pass


@dashboard.route('/', methods=['GET', 'POST'])
def index():
    minion_status = salt.execution_command_low(client='runner', fun='manage.status',
                                               kwargs={"timeout": 1, 'gather_job_timeout': 1})
    job_status = salt.execution_command_low(client='runner', fun='jobs.active')
    return render_template('dashboard/dashboard.html', job_status=job_status, minion_status=minion_status)
