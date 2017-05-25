from flask import Blueprint, render_template
from flask_login import login_required
from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, SelectField
from ButterSalt import salt


class Mid:
    def __init__(self, tgt):
        self.tgt = tgt

    def get_uptime(self):
        data = salt.execution_command_low(tgt=self.tgt, fun="status.uptime")
        return data

    def get_grains(self):
        data = salt.execution_command_low(tgt=self.tgt, fun="grains.items")
        return data


class StateForm(FlaskForm):
    salt_states = BooleanField('选择模板')
    salt_states_nfs = SelectField('nfs', choices=[('nfs-client', 'nfs-client'), ('nfs-server', 'nfs-server'),
                                                  (None, "")], option_widget=None)
    submit = SubmitField('提交')


cmdb = Blueprint('cmdb', __name__, url_prefix='/cmdb')


@cmdb.route('/')
@login_required
def index():
    data = salt.execution_command_low(client='runner', fun="manage.status")
    return render_template('cmdb/index.html', up=data['up'], down=data['down'])


@cmdb.route('/manage/')
@cmdb.route('/manage/<mid>', methods=['GET', 'POST'])
@login_required
def manage(mid=None):
    mid_grains = Mid(mid)
    return render_template('cmdb/manage.html', uptime=mid_grains.get_uptime()[mid],
                           grains=mid_grains.get_grains()[mid])
