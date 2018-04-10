# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, request
from deployer.app import app, file_operations, db
from deployer.app.forms import LoginForm, RegistrationForm
from deployer.app.config import Config
from deployer.app.models import User
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
@login_required
def index():
    sborki = file_operations.match_selection(Config.path, "*zip")
    return render_template('index.html', title='Home', sborki=sborki)


@app.route('/variables')
@login_required
def variables():
    variables = ['one_shit', 'some_shit', 'another_shit', 'more_shit']
    components = Config.GFcomponents
    return render_template('variables.html', title='Home', vars=variables, comps=components)


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
    return render_template('login.html', title='Войти', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


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



