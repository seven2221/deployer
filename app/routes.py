# -*- coding: utf-8 -*-
from flask import render_template, session, redirect, url_for, request
from app import app, file_operations, gf_operations, gf_variables
from app.forms import HostForm, ZipForm
from app.config import Config


##########  раскомментить если потребуется авторизация  ##########
# from flask import flash
# from app import db
# from app.forms import LoginForm, RegistrationForm
# from app.models import User
# from app.gf_operations import check_variables
# from flask_login import current_user, login_user, logout_user, login_required
# from werkzeug.urls import url_parse


class result(object):
    result = ""
    undeploy_result = ""


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
# @login_required   ##########  раскомментить если потребуется авторизация  ##########
def index():
    current_url = "http://" + Config.host + ":5000/index"
    sborki = file_operations.match_selection(Config.path, "*zip")
    form = HostForm()
    if form.validate_on_submit():
        session['host'] = form.host.data
        session['port'] = form.port.data
    return render_template('index.html', form=form, title='Home', current_url=current_url, sborki=sborki)


##########  раскомментить если потребуется авторизация  ##########
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if user is None or not user.check_password(form.password.data):
#             flash('Ошибка при вводе логина или пароля')
#             return redirect(url_for('login'))
#         login_user(user, remember=form.remember_me.data)
#         next_page = request.args.get('next')
#         if not next_page or url_parse(next_page).netloc != '':
#             next_page = url_for('index')
#         return redirect(next_page)
#     return render_template('login.html', title='Login', form=form)


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         user = User(username=form.username.data, email=form.email.data)
#         user.set_password(form.password.data)
#         db.session.add(user)
#         db.session.commit()
#         flash('Congratulations, you are now a registered user!')
#         return redirect(url_for('login'))
#     return render_template('register.html', title='Register', form=form)


# @app.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('login'))


@app.route('/check_prepare', methods=['GET', 'POST'])
# @login_required   ##########  раскомментить если потребуется авторизация  ##########
def check_prepare():
    form = ZipForm()
    sborki = file_operations.match_selection(Config.path, "*zip")
    return render_template('check_prepare.html', title='Variables', sborki=sborki, form=form)


@app.route('/variables', methods=['GET', 'POST'])
# @login_required   ##########  раскомментить если потребуется авторизация  ##########
def variables():
    sborki = file_operations.match_selection(Config.path, "*zip")
    host = session.get('host')
    variables = gf_variables.find_new_variables()
    components = Config.GFcomponents
    return render_template('variables.html', title='Variables', vars=variables, comps=components, host=host, sborki=sborki,result=result.result)


@app.route('/configurations', methods=['GET', 'POST'])
# @login_required   ##########  раскомментить если потребуется авторизация  ##########
def configurations():
    sborki = file_operations.match_selection(Config.path, "*zip")
    return render_template('configurations.html', title='Configurations',  sborki=sborki)


@app.route('/SA_menu', methods=['GET', 'POST'])
# @login_required   ##########  раскомментить если потребуется авторизация  ##########
def SA_menu():
    SAs = gf_operations.check_SA()
    return render_template('SA_menu.html', title='SA_menu', SAs=SAs)


@app.route('/deploy', methods=['GET', 'POST'])
# @login_required   ##########  раскомментить если потребуется авторизация  ##########
def deploy():
    sborki = file_operations.match_selection(Config.path, "*zip")
    return render_template('deploy.html', title='Deploy', sborki=sborki)


@app.route('/clean_session')
# @login_required   ##########  раскомментить если потребуется авторизация  ##########
def clean_session():
    session.pop('host')
    session.pop('port')
    return redirect(url_for('index'))


@app.route('/unpack', methods=['POST'])
# @login_required   ##########  раскомментить если потребуется авторизация  ##########
def unpack():
    session['zip'] = ""
    file_operations.deleter(Config.tempdir)
    zip_to_unpack = request.form['zip_to_unpack']
    session['zip'] = zip_to_unpack
    file_operations.unpack_zip(zip_to_unpack)
    return redirect(url_for('check_prepare'))


@app.route('/create_variable', methods=['GET', 'POST'])
# @login_required   ##########  раскомментить если потребуется авторизация  ##########
def create_variable():
    component = request.form['component']
    variable = request.form['variable']
    value = request.form['value']
    result.result = gf_operations.create_variable(component, variable, value)
    return redirect(url_for('variables'))


@app.route('/undeploy_SA', methods=['GET', 'POST'])
# @login_required   ##########  раскомментить если потребуется авторизация  ##########
def undeploy_SA():
    SA = request.form['SA']
    result.undeploy_result = gf_operations.undeploy_SA(SA)
    return redirect(url_for('SA_menu'))


@app.route('/stop_SA', methods=['GET', 'POST'])
# @login_required   ##########  раскомментить если потребуется авторизация  ##########
def stop_SA():
    SA = request.form['SA']
    result.undeploy_result = gf_operations.stop_SA(SA)
    return redirect(url_for('SA_menu'))


@app.route('/shutdown_SA', methods=['GET', 'POST'])
# @login_required   ##########  раскомментить если потребуется авторизация  ##########
def shutdown_SA():
    SA = request.form['SA']
    result.undeploy_result = gf_operations.shutdown_SA(SA)
    return redirect(url_for('SA_menu'))


@app.route('/start_SA', methods=['GET', 'POST'])
# @login_required   ##########  раскомментить если потребуется авторизация  ##########
def start_SA():
    SA = request.form['SA']
    result.undeploy_result = gf_operations.start_SA(SA)
    return redirect(url_for('SA_menu'))
