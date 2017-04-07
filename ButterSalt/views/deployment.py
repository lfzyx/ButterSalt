from flask import Blueprint, flash, redirect, url_for
from flask_login import login_required
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import InputRequired
import jenkins
from ButterSalt import J_server, db
from ButterSalt.models import ProductApplications
from pathlib import Path
import re


class Application(FlaskForm):
    application = SelectField('添加可用Application')
    submit = SubmitField('添加')


class SaltState(FlaskForm):
    state = StringField('state', validators=[InputRequired('名称是必填的')])
    submit = SubmitField('添加')


class TextEdit(FlaskForm):
    content = TextAreaField('Content', validators=[InputRequired('内容是必填的')])
    submit = SubmitField('保存')


deployment = Blueprint('deployment', __name__, url_prefix='/deployment')


@deployment.route('/product/', methods=['GET', 'POST'])
@login_required
def product():
    jobs = J_server.get_jobs()
    l = list()
    for n in jobs:
        l.append(tuple([n['name'], n['fullname']]))
    form = Application()
    form.application.choices = l
    if form.validate_on_submit():
        application = form.application.data
        execute = ProductApplications(application, 1, 'env', 'lfzyx', None, '2017')
        db.session.add(execute)
        db.session.commit()
        flash('添加成功')
        return redirect(url_for('deployment.product'))
    jobs = dict()
    for n in ProductApplications.query.all():
        try:
            jobs[n.name] = J_server.get_job_info(n.name)['lastSuccessfulBuild']['number']
        except jenkins.NotFoundException as err:
            print('jenkins exception: {0}'.format(err))
    return render_template('deployment/product.html', jobs=jobs, form=form)


@deployment.route('/product/deployconfig/',  methods=['GET', 'POST'])
@deployment.route('/product/deployconfig/<files>/',  methods=['GET', 'POST'])
@deployment.route('/product/deployconfig/<files>/<file>',  methods=['GET', 'POST'])
@login_required
def product_deployconfig(files=None, file=None):
    p = Path('file/deployconfig')
    if not p.exists():
        p.mkdir(parents=True)
    _subdirectories = [x.name for x in p.iterdir() if x.is_dir()]

    if file:
        q = p / files / file
        form = TextEdit()
        if form.validate_on_submit():
            with q.open(mode='w') as f:
                f.write(form.content.data)
            return redirect(url_for('deployment.product_deployconfig', files=files))
        with q.open() as f:
            text = f.readlines()
        return render_template('deployment/product_deployconfig_files_edit.html', text=text, form=form)

    if files:
        q = p / files
        _files = [x.name for x in q.iterdir() if not re.match('^\.', x.name)]
        return render_template('deployment/product_deployconfig_files.html', files=_files)

    return render_template('deployment/product_deployconfig.html', subdirectories=_subdirectories)


@deployment.route('/system/')
@login_required
def system():
    return render_template('deployment/system.html')


@deployment.route('/system/add', methods=['GET', 'POST'])
@login_required
def system_add():
    form = SaltState()
    if form.validate_on_submit():
        flash('添加成功')
        return redirect(url_for('deployment.system'))
    return render_template('deployment/system_add.html', form=form)
