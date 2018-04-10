# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, request
from app import app, file_operations, db, gf_operations
from app.forms import LoginForm, RegistrationForm, HostForm
from app.config import Config
from app.models import User
from app.gf_operations import check_variables
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
@login_required
def index():
    form = HostForm
    # if form.validate_on_submit():
    #     host =
    return render_template('index.html', form=form, title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Ошибка при вводе логина или пароля')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/variables', methods=['GET', 'POST'])
@login_required
def variables():
    variables = ['one_shit', 'some_shit', 'another_shit', 'more_shit']
    # variables = check_variables.find_new_variables("ms-glass030")
    components = Config.GFcomponents
    return render_template('variables.html', title='Variables', vars=variables, comps=components)


@app.route('/configurations', methods=['GET', 'POST'])
@login_required
def configurations():
    return render_template('configurations.html', title='Configurations')


@app.route('/undeploy', methods=['GET', 'POST'])
@login_required
def undeploy():
    SAs = ['comverseProxy', 'APS', 'MAE', 'shit']
    # SAs = gf_operations.check_SA("ms-glass030")
    return render_template('undeploy.html', title='Undeploy', SAs=SAs)


@app.route('/deploy', methods=['GET', 'POST'])
@login_required
def deploy():
    sborki = file_operations.match_selection(Config.path, "*zip")
    return render_template('deploy.html', title='Deploy', sborki=sborki)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)



