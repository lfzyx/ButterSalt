from flask import flash, redirect, url_for
from flask_login import login_required
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired
from ButterSalt import J_server
from ButterSalt.models import ProductApplications, ProductApplicationsConfigurations
from pathlib import Path
import re
from . import deployment


class FormSystemApplicationConfiguration(FlaskForm):
    configuration_name = StringField('配置名称', validators=[InputRequired('名称是必填的')])
    bind_host = StringField('绑定主机', validators=[InputRequired('名称是必填的')])
    submit = SubmitField('保存')


class TextEdit(FlaskForm):
    content = TextAreaField('Content', validators=[InputRequired('内容是必填的')])
    submit = SubmitField('保存')


@deployment.route('/product/', methods=['GET', 'POST'])
@login_required
def product():
    listdata = list()
    for application in J_server.get_jobs():
        try:
            listdata.append({'name': application.get('name'),
                             'lastSuccessfulBuild': J_server.get_job_info(application.get('name'))['lastSuccessfulBuild']['number'],
                             'host': ProductApplications.query.filter_by(name=application.get('name')).count()
                             })
        except TypeError:
            listdata.append({'name': None, 'lastSuccessfulBuild': None, 'host': None})
    return render_template('deployment/product.html', list=listdata)


@deployment.route('/product/<name>/', methods=['GET', 'POST'])
@login_required
def product_name(name=None):
    listdata = list()
    for application in ProductApplications.query.filter_by(name=name).all():
        listdata.append({'name': application.name, 'bind_host': application.applicationhost.name,
                         'delivery_version': application.delivery_version, 'role': application.applicationhost.role})
    return render_template('deployment/product_detail.html', list=listdata)


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
