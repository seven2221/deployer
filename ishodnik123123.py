import zipfile
import os
import fnmatch
import subprocess
import logging.handlers
import time
from flask import Flask, render_template



path = "C:\\Users\\IOnoshko\\Documents\\Test\\deploy\\"
tempdir = path + "temp\\temp"

# логирование
logtime = time.strftime('%Y%m%d')
logging_file = (path + 'deploy_' + logtime + '.log')  # файл, в который пишем лог
formatter = logging.Formatter('[%(asctime)s][%(levelname)-4s] : %(message)s', datefmt='%d/%m/%Y %H:%M:%S')  # формат лога
handlers = \
    [
        logging.handlers.RotatingFileHandler
            (
                logging_file,
                encoding='utf8',
                maxBytes=100000,
                backupCount=1
            ),
        logging.StreamHandler()
    ]
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
for handler in handlers:
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    root_logger.addHandler(handler)


host = input('host --> ')
logging.debug("Start deploying " + "(name.version) " + " on " + host + " =============================================================")


class selectors:

    @classmethod
    def match_selection(cls, dir, match):
        filelist = os.listdir(dir)
        results = []
        for name in filelist:
            if fnmatch.fnmatch(name, match):
                results.append(name)
        yield results


class old_variables:
    components = ['sun-bpel-engine', 'sun-http-binding', 'sun-jms-binding', 'sun-database-binding', 'sun-file-binding', 'sun-ftp-binding', 'sun-scheduler-binding']
    allvariables = []
    allconfigs = []

    @classmethod
    def find_variables(cls):
        for component in old_variables.components:
            total_variables = subprocess.Popen(["asadmin", 'list-jbi-application-variables',"--component", component, "--host", host, "--port", "4848", "--user", "admin", "--passwordfile", "D:\\Glassfish22\\passfile"], stdout=subprocess.PIPE, shell=True)
            for line in total_variables.stdout:
                if "executed successfully." not in str(line) and "Nothing to list" not in str(line):
                    variable = str(line).split("=")[0].replace("b\'", "").replace("b\"", "").replace(" ", "")
                    if variable not in old_variables.allvariables:
                        old_variables.allvariables.append(variable)

    @classmethod
    def find_configs(cls):
        for component in old_variables.components:
            total_configs = subprocess.Popen(["asadmin", 'list-jbi-application-configurations',"--component", component, "--host", host, "--port", "4848", "--user", "admin", "--passwordfile", "D:\\Glassfish22\\passfile"], stdout=subprocess.PIPE, shell=True)
            for line in total_configs.stdout:
                if "executed successfully." not in str(line) and "ERROR" not in str(line):
                    configuration = str(line).replace("b\'", "").replace("\\r\\n'", "").replace(" ", "")
                    if configuration not in old_variables.allconfigs:
                        old_variables.allconfigs.append(configuration)
                        logging.debug("configuration === " + configuration)

    @classmethod
    def main(cls):
        old_variables.find_variables()
        old_variables.find_configs()


class new_variables:
    variables = []
    configurations = []

    @staticmethod
    def findvariables():
        os.chdir(tempdir)
        for jarFiles in selectors.match_selection(tempdir, "*jar"):
            for jarFile in jarFiles:
                jar_with_variables = zipfile.ZipFile(jarFile, 'r')
                jar_with_variables_filelist = jar_with_variables.infolist()
                for file in jar_with_variables_filelist:
                    filename = file.filename
                    with zipfile.ZipFile(jarFile) as jar_to_open:
                        with jar_to_open.open(filename) as opened_file:

                            for line in opened_file:
                                if filename.endswith('.bpel'):
                                    if "literal>" in str(line):
                                        variable = str(line).split("literal")[1].replace(">${", "").replace("}</", "")
                                        if variable not in new_variables.variables:
                                            new_variables.variables.append(variable)
                                else:
                                    if "${" in str(line):
                                        variable = str(line).split("${")[1].split("}")[0]
                                        if variable not in new_variables.variables and variable != "HttpDefaultPort" and "\\" not in variable: #len(variable) < 50:
                                            new_variables.variables.append(variable)
                                    if "<application-config" in str(line):
                                        configuration = str(line).split("\"")[3]
                                        if configuration not in new_variables.configurations and configuration not in new_variables.variables:
                                            new_variables.configurations.append(configuration)

    @staticmethod
    def main():
        for zips in selectors.match_selection(path, "*zip"):
            for zip in zips:
                with zipfile.ZipFile(path + zip) as zipzip:
                    zipzip.extractall(tempdir)
                    zipzip.close()
                    new_variables.findvariables()
                # временное логирование
                for variable in new_variables.variables:
                    logging.debug("find other new variable " + variable)
                for congiguration in new_variables.configurations:
                    logging.debug("find new configuration " + congiguration)
                for old in old_variables.allvariables:
                    logging.debug("find existed variable " + old)


class main:

    @classmethod
    def add_variables_to_gf(cls):
        for variable in new_variables.variables:
            if variable in old_variables.allvariables:
                logging.debug(variable + " already exists on " + host)
            else:
                component = input("добавление переменной " + variable + " \nукажите компонент(байндинг):")
                value = input("укажите значение: ")
                logging.debug("asadmin add-variable бла бла бла " + variable + " " + component + " " + value)

    @classmethod
    def add_configurations_to_gf(cls):
        for configuration in new_variables.configurations:
            if configuration in old_variables.allconfigs:
                logging.debug(configuration + " already exists on " + host)
            else:
                component = input("добавление конфигурации " + configuration + " \nукажите компонент(байндинг):")
                value = input("укажите значение: ")
                logging.debug("asadmin add-configuration бла бла бла " + configuration + " " + component + " " + value)


    @classmethod
    def deployer(cls):
        new_variables.main()
        old_variables.main()

        main.add_variables_to_gf()

        main.add_configurations_to_gf()

        for zips in selectors.match_selection(path, "*zip"):
            for zip in zips:
             logging.debug("subprocess asadmin deploy " + zip)




app = Flask(__name__)

@app.route('/')
def index():
  return render_template('template.html')


@app.route('/my-link/')
def my_link():
    name = "Alan"
    print('I got clicked!')
    return render_template('test.html', name=name)


@app.route('/deployer/')
def call_deployer():
    sborki = list(selectors.match_selection(path, "*zip"))[0]
    new_variables.main()
    vars = new_variables.variables
    print('call deployer')
    return render_template('deployer.html', vars=vars, sborki=sborki)


@app.route('/deployer/variables')
def call_deployer_variables():
    new_variables.main()
    vars = new_variables.variables
    print('call deployer')
    return render_template('variables.html', vars=vars)


if __name__ == '__main__':
    app.run(host='10.127.242.206', debug=True)


#main.deployer()
logging.debug("Deploying of " + "(name.version) " + " on " + host + " is finished ====================================================")





