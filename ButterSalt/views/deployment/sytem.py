from flask import flash, redirect, url_for, session, request
from flask_login import login_required
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired
from ButterSalt import db, salt
from ButterSalt import models
import datetime
from . import deployment


class FormSystemApplication(FlaskForm):
    name = StringField('应用名称', validators=[InputRequired('名称是必填的')])
    submit = SubmitField('保存')


class FormSystemApplicationConfiguration(FlaskForm):
    configuration_name = StringField('配置名称', validators=[InputRequired('名称是必填的')])
    bind_host = StringField('绑定主机', validators=[InputRequired('名称是必填的')])
    submit = SubmitField('保存')


class TextEdit(FlaskForm):
    content = TextAreaField('Content', validators=[InputRequired('内容是必填的')])
    submit = SubmitField('保存')


@deployment.route('/system/')
@login_required
def system():
    listdata = list()
    for application in models.SystemApplications.query.all():
        listdata.append({'name': application.name, 'bind_configurations': application.configurations.count()})
    return render_template('deployment/system.html', list=listdata)


@deployment.route('/system/add', methods=['GET', 'POST'])
@login_required
def system_add():
    form = FormSystemApplication()
    if form.validate_on_submit():
        name = form.name.data
        execute = models.SystemApplications(
            name=name, creator=models.Users.query.filter_by(username=session['username']).one_or_none().id,
            modifer=None,
            last_modify_time=datetime.datetime.now())
        db.session.add(execute)
        db.session.commit()
        flash('保存成功')
        return redirect(url_for('deployment.system'))
    return render_template('deployment/system_add.html', form=form)


@deployment.route('/system/<name>/', methods=['GET', 'POST'])
@login_required
def system_name(name=None):
    listdata = list()
    for configuration in models.SystemApplications.query.filter_by(name=name).one_or_none().configurations:
        listdata.append({'id': configuration.id, 'name': configuration.name, 'bind_host': configuration.bind_host,
                         'last_modify_time': configuration.last_modify_time})
    if request.method == 'POST':
        if 'delete' in request.form:
            models.SystemApplicationsConfigurations.query.filter_by(id=request.form.get('delete')).delete()
            db.session.commit()
            return redirect(url_for('deployment.system_name', name=name))
    return render_template('deployment/system_configuration.html', list=listdata)


@deployment.route('/system/<name>/add', methods=['GET', 'POST'])
@login_required
def system_configuration_add(name=None):
    form = FormSystemApplicationConfiguration()
    if form.validate_on_submit():
        configuration_name = form.configuration_name.data
        bind_host = form.bind_host.data
        # salt.execution_command_minions(tgt=bind_host, fun='state.apply', args=name)
        # 防止sls文件被覆盖
        try:
            text = salt.read_pillar_file(configuration_name + '.sls')['return'][0][
                '/srv/pillar/' + configuration_name + '.sls']
        except IndexError:
            text = ""
        salt.write_pillar_file(text, configuration_name + '.sls')
        execute = models.SystemApplicationsConfigurations(
            name=configuration_name,
            bind_application=models.SystemApplications.query.filter_by(name=name).one_or_none().id,
            bind_host=bind_host, version='1', creator=models.Users.query.filter_by(username=session['username']).one_or_none().id,
            modifer=None, last_modify_time=datetime.datetime.now())
        db.session.add(execute)
        db.session.commit()
        flash('保存成功')
        return redirect(url_for('deployment.system_name', name=name))
    return render_template('deployment/system_configuration_add.html', form=form)


@deployment.route('/system/<name>/<configuration>', methods=['GET', 'POST'])
@login_required
def system_configuration_edit(name=None, configuration=None):
    try:
        text = salt.read_pillar_file(configuration+'.sls')['return'][0]['/srv/pillar/'+configuration+'.sls']
    except IndexError:
        text = ""
    form = TextEdit()
    if form.validate_on_submit():
        salt.write_pillar_file(form.content.data, configuration+'.sls')
        models.SystemApplicationsConfigurations.query.filter_by(name=configuration).update({"last_modify_time":datetime.datetime.now()})
        db.session.commit()
        flash('保存成功')
        return redirect(url_for('deployment.system_name', name=name))
    return render_template('deployment/system_configuration_edit.html', text=text, form=form)