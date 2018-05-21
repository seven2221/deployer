# -*- coding: utf-8 -*-
from app import app
from app.config import Config

app.run(host=Config.host)


# from app import app, db
# from app.models import User
#
# @app.shell_context_processor
# def make_shell_context():
#     return {'db': db, 'User': User}