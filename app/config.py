# -*- coding: utf-8 -*-
import os
# import mysql
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'glassfish123'

    path_to_zip = ""

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://glassfish:kem7Hdowm8d@ms-glass012/deployer'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

