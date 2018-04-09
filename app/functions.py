import zipfile
import os
import subprocess
import logging.handlers
from app import Config, selectors, logger


class old_variables:
    components = ['sun-bpel-engine', 'sun-http-binding', 'sun-jms-binding', 'sun-database-binding', 'sun-file-binding', 'sun-ftp-binding', 'sun-scheduler-binding']
    allvariables = []
    allconfigs = []

    @classmethod
    def find_variables(cls, host):
        for component in old_variables.components:
            total_variables = subprocess.Popen(["asadmin", 'list-jbi-application-variables',"--component", component, "--host", host, "--port", "4848", "--user", "admin", "--passwordfile", "D:\\Glassfish22\\passfile"], stdout=subprocess.PIPE, shell=True)
            for line in total_variables.stdout:
                if "executed successfully." not in str(line) and "Nothing to list" not in str(line):
                    variable = str(line).split("=")[0].replace("b\'", "").replace("b\"", "").replace(" ", "")
                    if variable not in old_variables.allvariables:
                        old_variables.allvariables.append(variable)

    @classmethod
    def find_configs(cls, host):
        for component in old_variables.components:
            total_configs = subprocess.Popen(["asadmin", 'list-jbi-application-configurations',"--component", component, "--host", host, "--port", "4848", "--user", "admin", "--passwordfile", "D:\\Glassfish22\\passfile"], stdout=subprocess.PIPE, shell=True)
            for line in total_configs.stdout:
                if "executed successfully." not in str(line) and "ERROR" not in str(line):
                    configuration = str(line).replace("b\'", "").replace("\\r\\n'", "").replace(" ", "")
                    if configuration not in old_variables.allconfigs:
                        old_variables.allconfigs.append(configuration)

    @staticmethod
    def main(host):
        old_variables.find_variables(host)
        old_variables.find_configs(host)


class new_variables:
    variables = []
    configurations = []

    @staticmethod
    def findvariables():
        os.chdir(Config.tempdir)
        for jarFiles in selectors.match_selection(Config.tempdir, "*jar"):
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
                                        if variable not in new_variables.variables and variable != "HttpDefaultPort" and "\\" not in variable:  # len(variable) < 50:
                                            new_variables.variables.append(variable)
                                    if "<application-config" in str(line):
                                        configuration = str(line).split("\"")[3]
                                        if configuration not in new_variables.configurations and configuration not in new_variables.variables:
                                            new_variables.configurations.append(configuration)

    @staticmethod
    def main():
        for zips in selectors.match_selection(Config.path, "*zip"):
            for zip in zips:
                with zipfile.ZipFile(Config.path + zip) as zipzip:
                    zipzip.extractall(Config.tempdir)
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
    def add_variables_to_gf(cls, host):
        for variable in new_variables.variables:
            if variable in old_variables.allvariables:
                logging.debug(variable + " already exists on " + host)
            else:
                component = input("добавление переменной " + variable + " \nукажите компонент(байндинг):")
                value = input("укажите значение: ")
                logging.debug("asadmin add-variable бла бла бла " + variable + " " + component + " " + value)

    @classmethod
    def add_configurations_to_gf(cls, host):
        for configuration in new_variables.configurations:
            if configuration in old_variables.allconfigs:
                logging.debug(configuration + " already exists on " + host)
            else:
                component = input("добавление конфигурации " + configuration + " \nукажите компонент(байндинг):")
                value = input("укажите значение: ")
                logging.debug("asadmin add-configuration бла бла бла " + configuration + " " + component + " " + value)


    @classmethod
    def deployer(cls, host):
        new_variables.main()
        old_variables.main(host)

        main.add_variables_to_gf(host)

        main.add_configurations_to_gf(host)

        for zips in selectors.match_selection(Config.path, "*zip"):
            for zip in zips:
             logging.debug("subprocess asadmin deploy " + zip)
