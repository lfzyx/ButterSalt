from flask import Blueprint, flash, redirect, url_for, request
from flask_login import login_required
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired
from ButterSalt import J_server, db
from ButterSalt.models import JenkinsJobs
from pathlib import Path


class Job(FlaskForm):
    job = StringField('job', validators=[InputRequired('名称是必填的')])
    submit = SubmitField('添加')


class SaltState(FlaskForm):
    state = StringField('state', validators=[InputRequired('名称是必填的')])
    submit = SubmitField('添加')


class TextEdit(FlaskForm):
    content = TextAreaField('Content', validators=[InputRequired('内容是必填的')])
    submit = SubmitField('保存')


deployment = Blueprint('deployment', __name__, url_prefix='/deployment')


@deployment.route('/operation/', methods=['GET', 'POST'])
@login_required
def operation():
    jobs = dict()
    for n in JenkinsJobs.query.all():
        jobs[n.job_name] = J_server.get_job_info(n.job_name)['lastSuccessfulBuild']['number']
    return render_template('deployment/operation.html', jobs=jobs)


@deployment.route('/operation/add', methods=['GET', 'POST'])
@login_required
def operation_add():
    form = Job()
    if form.validate_on_submit():
        job = form.job.data
        execute = JenkinsJobs(job, None)
        db.session.add(execute)
        db.session.commit()
        flash('添加成功')
        return redirect(url_for('deployment.operation'))
    return render_template('deployment/operation_add.html', form=form)


@deployment.route('/operation/deployconfig/',  methods=['GET', 'POST'])
@deployment.route('/operation/deployconfig/<files>/',  methods=['GET', 'POST'])
@deployment.route('/operation/deployconfig/<files>/<file>',  methods=['GET', 'POST'])
@login_required
def operation_deployconfig(files=None, file=None):
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
            return redirect(url_for('deployment.operation_deployconfig', files=files))
        with q.open() as f:
            text = f.readlines()
        return render_template('deployment/operation_deployconfig_files_edit.html', text=text, form=form)

    if files:
        q = p / files
        _files = [x.name for x in q.iterdir()]
        return render_template('deployment/operation_deployconfig_files.html', files=_files)

    return render_template('deployment/operation_deployconfig.html', subdirectories=_subdirectories)


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
