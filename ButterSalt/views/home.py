from flask import render_template, redirect, url_for, flash, Blueprint
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Optional
from flask_wtf import FlaskForm
from flask_login import login_required
from ButterSalt.models import MoudleExecuteHistory
from ButterSalt import Token, app, db
import json


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
    keyarg = StringField('键', validators=[Optional()])
    wordarg = StringField('值', validators=[Optional()])
    submit = SubmitField('提交')


home = Blueprint('home', __name__)


@home.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = ModulesForm()
    if form.validate_on_submit():
        tgt = form.tgt.data
        fun = form.fun.data
        arg = form.arg.data.split()
        keyarg = form.keyarg.data
        wordarg = form.wordarg.data
        if wordarg == 'True':
            wordarg = True
        elif wordarg == 'False':
            wordarg = False
        if keyarg:
            kwarg = {keyarg: wordarg}
        else:
            kwarg = {}
        jid = Token.post(app.config.get('SALT_API') + '/minions/', json={
            'tgt': tgt,
            'fun': fun,
            'arg': arg,
            'kwarg': kwarg,
        }).json()['return'][0]['jid']
        flash('执行完成')
        execute = MoudleExecuteHistory(tgt, fun, str(arg), str(kwarg), 1)
        db.session.add(execute)
        db.session.commit()
        return redirect(url_for('saltstack.jobs', jid=jid))
    data = Token.get(app.config.get('SALT_API') + '/').json()
    minions = Token.get(app.config.get('SALT_API') + '/keys').json()
    return render_template('home/index.html', Data=data, Minions=json.dumps(minions['return']['minions']), form=form)
