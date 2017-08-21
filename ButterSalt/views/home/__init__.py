from flask import render_template, redirect, url_for, flash, Blueprint
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Optional
from flask_wtf import FlaskForm
from flask_login import login_required
from ButterSalt import models, db, salt


class ModulesForm(FlaskForm):
    """ SaltStack Remote Execution form.

    When you want execute salt modules in web gui, you need a form.
    This form provide target, module.function, arguments.
    See (https://docs.saltstack.com/en/getstarted/fundamentals/remotex.html).
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
    """ Generate ModulesForm, provide autocomplete required data-source.

    data-source is tgt_list, comes from method salt.get_accepted_keys.
    Why provide accepted_keys as autocomplete data-source, not based on the what hosts are up？
    I think is that operator do not need to judgment hosts status,
    they just need to know which salt modules should be execution on which hosts.
    """
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
        execute = models.SaltExecuteHistory(tgt=tgt, fun=fun, args=str(arg), kwargs=str(d), user=1)
        db.session.add(execute)
        db.session.commit()
        flash('执行完成')
        return redirect(url_for('saltstack.jobs', jid=jid))
    tgt_list = salt.get_accepted_keys()
    return render_template('home/index.html', tgt_list=tgt_list, form=form)
