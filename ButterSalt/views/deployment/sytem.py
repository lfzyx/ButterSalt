from flask import flash, redirect, url_for, session, request
from flask_login import login_required
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired
from ButterSalt import db, salt
from ButterSalt.models import SystemApplications, SystemApplicationsConfigurations, Users
import datetime
import json
from . import deployment


class FormSystemApplication(FlaskForm):
    name = StringField('应用名称', validators=[InputRequired('名称是必填的')])
    submit = SubmitField('保存')


class FormSystemApplicationConfiguration(FlaskForm):
    pillar = TextAreaField('配置名称')
    bind_host = StringField('绑定主机', validators=[InputRequired('主机名是必填的')])
    submit = SubmitField('保存')


class TextEdit(FlaskForm):
    content = TextAreaField('Content', validators=[InputRequired('内容是必填的')])
    submit = SubmitField('保存')


@deployment.route('/system/')
@login_required
def system():
    listdata = list()
    for application in SystemApplications.query.all():
        listdata.append({'name': application.name, 'bind_configurations': application.configurations.count()})
    return render_template('deployment/system.html', list=listdata)


@deployment.route('/system/add', methods=['GET', 'POST'])
@login_required
def system_add():
    form = FormSystemApplication()
    if form.validate_on_submit():
        name = form.name.data
        execute = SystemApplications(
            name=name, creator=Users.query.filter_by(username=session['username']).one_or_none().id,
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
    for configuration in SystemApplications.query.filter_by(name=name).one_or_none().configurations:
        listdata.append({'id': configuration.id, 'pillar': configuration.pillar, 'bind_host': configuration.bind_host,
                         'last_modify_time': configuration.last_modify_time})
    if request.method == 'POST':
        if 'delete' in request.form:
            SystemApplicationsConfigurations.query.filter_by(id=request.form.get('delete')).delete()
            db.session.commit()
            return redirect(url_for('deployment.system_name', name=name))
        elif 'modify' in request.form:
            return redirect(url_for('deployment.system_configuration_edit', name=name, id=request.form.get('modify')))
        elif 'apply' in request.form:
            apply = SystemApplicationsConfigurations.query.filter_by(id=request.form.get('apply')).one_or_none()
            bind_host = apply.bind_host
            bind_application = apply.applications.name
            pillar = {'pillar': json.loads(apply.pillar)}
            jid = salt.execution_command_minions(
                tgt=bind_host, fun='state.apply', args=[bind_application], kwargs=pillar)
            flash('执行完成')
            return redirect(url_for('saltstack.jobs', jid=jid))
    return render_template('deployment/system_configuration.html', list=listdata)


@deployment.route('/system/<name>/add', methods=['GET', 'POST'])
@login_required
def system_configuration_add(name=None):
    form = FormSystemApplicationConfiguration()
    if form.validate_on_submit():
        pillar = form.pillar.data
        bind_host = form.bind_host.data
        execute = SystemApplicationsConfigurations(
            bind_application=SystemApplications.query.filter_by(name=name).one_or_none().id,
            bind_host=bind_host, version='1',
            pillar=pillar,
            creator=Users.query.filter_by(username=session['username']).one_or_none().id,
            modifer=None, last_modify_time=datetime.datetime.now())
        db.session.add(execute)
        db.session.commit()
        flash('保存成功')
        return redirect(url_for('deployment.system_name', name=name))
    tgt_list = salt.get_accepted_keys()
    return render_template('deployment/system_configuration_add.html', tgt_list=tgt_list, form=form)


@deployment.route('/system/<name>/edit', methods=['GET', 'POST'])
@login_required
def system_configuration_edit(name=None):
    config_id = request.args.get('id', '')
    pillar = SystemApplicationsConfigurations.query.filter_by(id=config_id).one_or_none().pillar
    form = TextEdit()
    if form.validate_on_submit():
        SystemApplicationsConfigurations.query.filter_by(id=config_id).update(
            {"pillar": form.content.data})
        SystemApplicationsConfigurations.query.filter_by(id=config_id).update(
            {"last_modify_time": datetime.datetime.now()})
        db.session.commit()
        flash('保存成功')
        return redirect(url_for('deployment.system_name', name=name))
    return render_template('deployment/system_configuration_edit.html', text=pillar, form=form)
