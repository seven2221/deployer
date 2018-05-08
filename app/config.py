# -*- coding: utf-8 -*-
import os


class Config(object):

    host = "10.127.242.204"

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'glassfish123'

    GFcomponents = ['sun-bpel-engine', 'sun-http-binding', 'sun-jms-binding', 'sun-database-binding', 'sun-file-binding', 'sun-ftp-binding', 'sun-scheduler-binding']

    home = "C:\\Users\\IOnoshko\\Documents\\Test\\deployer_home\\"
    zippath = home + "zipfiles\\"
    logpath = home + "logs\\"
    tempdir = home + "temp\\"

    passfile = home + "passfiles\\passfile"
    passfile_test1 = home + "passfiles\\passfile_test"
    passfile_test2 = home + "passfiles\\passfile_test2"
    passfile_test3 = home + "passfiles\\passfile_test3"

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://glassfish:kem7Hdowm8d@ms-glass012/deployer'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

