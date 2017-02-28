from flask import render_template, redirect, url_for, flash, Blueprint
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Optional
from flask_wtf import FlaskForm
from flask_login import login_required
from ButterSalt.models import MoudleExecuteHistory
from ButterSalt import db, salt


class ModulesForm(FlaskForm):
    """ SaltStack Remote Execution form.

    When you want execute salt modules in web gui, you need a form.
    This form provide target, module.function, arguments.
    See (https://docs.saltstack.com/en/getstarted/fundamentals/remotex.html).
    But sometimes you want use kwargs and don't kown need use ':' or '=', so resolve the kwargs into key and word
    """
    tgt = StringField('目标', validators=[InputRequired('目标是必须的')])
    fun = StringField('模块', validators=[InputRequired('模块是必须的')])
    arg = StringField('参数', validators=[Optional()])
    kwarg = StringField('键值', validators=[Optional()])
    submit = SubmitField('提交')


home = Blueprint('home', __name__)


@home.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = ModulesForm()
    if form.validate_on_submit():
        d = dict()
        tgt = form.tgt.data
        fun = form.fun.data
        arg = form.arg.data.split()
        kwarg = form.kwarg.data.split()
        for n in kwarg:
            kw = n.split('=')
            d[kw[0]] = kw[1]
        jid = salt.execution_command_minions(tgt=tgt, fun=fun, args=arg, kwargs=d)
        flash('执行完成')
        execute = MoudleExecuteHistory(tgt, fun, str(arg), str(d), 1)
        db.session.add(execute)
        db.session.commit()
        return redirect(url_for('saltstack.jobs', jid=jid))
    tgt_list = salt.get_accepted_keys()
    return render_template('home/index.html', tgt_list=tgt_list, form=form)
