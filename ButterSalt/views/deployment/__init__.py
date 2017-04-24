from flask import Blueprint, flash, redirect, url_for, session
from flask_login import login_required
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import InputRequired
import jenkins
from ButterSalt import J_server, db, salt
from ButterSalt import models
from pathlib import Path
import re
import datetime


class FormSystemApplication(FlaskForm):
    name = StringField('应用名称', validators=[InputRequired('名称是必填的')])
    bind_host = StringField('绑定主机')
    submit = SubmitField('保存')


class FormProductApplications(FlaskForm):
    name = StringField('应用名称', validators=[InputRequired('名称是必填的')])
    bind_host = StringField('绑定主机')
    bind_configuration_group = StringField('绑定配置')
    submit = SubmitField('保存')


class TextEdit(FlaskForm):
    content = TextAreaField('Content', validators=[InputRequired('内容是必填的')])
    submit = SubmitField('保存')


deployment = Blueprint('deployment', __name__, url_prefix='/deployment')


@deployment.route('/product/', methods=['GET', 'POST'])
@login_required
def product():
    jobs = dict()
    for n in models.ProductApplications.query.all():
        try:
            jobs[n.name] = J_server.get_job_info(n.name)['lastSuccessfulBuild']['number']
        except jenkins.NotFoundException as err:
            print('jenkins exception: {0}'.format(err))
    return render_template('deployment/product.html', jobs=jobs)


@deployment.route('/product/add', methods=['GET', 'POST'])
@login_required
def product_add():
    jobs = J_server.get_jobs()
    l = list()
    for n in jobs:
        l.append(tuple([n['name'], n['fullname']]))
    form = FormProductApplications()
    form.name.choices = l
    if form.validate_on_submit():
        name = form.name.data
        execute = models.ProductApplications(name, 1, 'env', 'lfzyx', None, '2017')
        db.session.add(execute)
        db.session.commit()
        flash('添加成功')
        return redirect(url_for('deployment.product'))
    return render_template('deployment/product_add.html', form=form)


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
@deployment.route('/system/<name>/')
@login_required
def system(name=None):
    if name:
        listdata = list()
        for n in models.SystemApplications.query.filter_by(name=name):
            listdata.append({'name': n.name, 'bind_host': n.bind_host,'last_modify_time': n.last_modify_time})
        return render_template('deployment/system.html', list=listdata)

    listdata = list()
    for n in models.SystemApplications.query.all():
        listdata.append({'name': n.name, 'bind_host': models.SystemApplications.query.filter_by(name=n.name).count()})
    listdata = [dict(t) for t in set([tuple(d.items()) for d in listdata])]
    return render_template('deployment/system.html', list=listdata)


@deployment.route('/system/add', methods=['GET', 'POST'])
@login_required
def system_add():
    form = FormSystemApplication()
    if form.validate_on_submit():
        name = form.name.data
        bind_host = form.bind_host.data
        if bind_host:
            salt.execution_command_minions(tgt=bind_host, fun='state.apply', args=name)
        execute = models.SystemApplications(
            name, bind_host, session['username'], None, datetime.datetime.now())
        db.session.add(execute)
        db.session.commit()
        flash('保存成功')
        return redirect(url_for('deployment.system'))
    return render_template('deployment/system_add.html', form=form)
