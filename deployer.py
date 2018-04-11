# -*- coding: utf-8 -*-
from app import app

app.run(host='10.127.242.208')


# from app import app, db
# from app.models import User
#
# @app.shell_context_processor
# def make_shell_context():
#     return {'db': db, 'User': User}