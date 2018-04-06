# -*- coding: utf-8 -*-
import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'glassfish123'

    path = "C:\\Users\\IOnoshko\\Documents\\Test\\deploy\\"
    logpath = path + "logs_of_some_shit\\"
    tempdir = path + "temp\\temp"

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://glassfish:kem7Hdowm8d@ms-glass012/deployer'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

