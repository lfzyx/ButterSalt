from flask import Blueprint, flash, redirect, url_for
from flask_login import login_required
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired
from ButterSalt import J_server, db
from ButterSalt.models import JenkinsJobs


class Job(FlaskForm):
    job = StringField('job', validators=[InputRequired('名称是必填的')])
    submit = SubmitField('添加')


class SaltState(FlaskForm):
    state = StringField('state', validators=[InputRequired('名称是必填的')])
    submit = SubmitField('添加')


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
