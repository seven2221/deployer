# -*- coding: utf-8 -*-
import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'glassfish123'

    GFcomponents = ['sun-bpel-engine', 'sun-http-binding', 'sun-jms-binding', 'sun-database-binding', 'sun-file-binding', 'sun-ftp-binding', 'sun-scheduler-binding']

    path = "C:\\Users\\IOnoshko\\Documents\\Test\\deploy\\"
    logpath = path + "logs_of_some_shit\\"
    tempdir = path + "temp\\"
    passfile = "D:\\Glassfish22\\passfile"
    passfile_test = "D:\\Glassfish22\\passfile123"

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://glassfish:kem7Hdowm8d@ms-glass012/deployer'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

