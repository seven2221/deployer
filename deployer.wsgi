import sys
import logging
#import os, sys

project_dir = "C:\\Users\\IOnoshko\\Documents\\GitRepos\\deployer\\"

#activate_this = os.path.join(PROJECT_DIR, 'venv3/bin', 'activate_this.py')
#execfile(activate_this, dict(__file__=activate_this))
#sys.path.insert(0, PROJECT_DIR)

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, project_dir)

from deployer import app as application
application.secret.key = "glassfish123"