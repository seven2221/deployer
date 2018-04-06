# -*- coding: utf-8 -*-
from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'glassfish'}
    sborki = ['test', 'test', 'test']
    vars = ['123', '123', '123', '123']
    return render_template('index.html', title='Home', user=user, sborki=sborki, vars=vars)
