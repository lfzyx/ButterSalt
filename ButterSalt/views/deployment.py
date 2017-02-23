from flask import Blueprint, flash, redirect, url_for
from flask_login import login_required
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired
from ButterSalt import app, Token
import jenkins


from ..models import JenkinsJobs
from .. import db

server = jenkins.Jenkins(
    app.config.get('JENKINS_API'),
    username=app.config.get('J_USERNAME'),
    password=app.config.get('J_PASSWORD')
)


class Job(FlaskForm):
    job = StringField('job', validators=[InputRequired('名称是必填的')])
    submit = SubmitField('添加')

deployment = Blueprint('deployment', __name__, url_prefix='/deployment')


@deployment.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = Job()
    if form.validate_on_submit():
        job = form.job.data
        execute = JenkinsJobs(job, None)
        db.session.add(execute)
        db.session.commit()
        flash('添加成功')
    jobs = dict()
    for n in JenkinsJobs.query.all():
        jobs[n.job_name] = server.get_job_info(n.job_name)['lastSuccessfulBuild']['number']
    return render_template('deployment/index.html', form=form, jobs=jobs)
